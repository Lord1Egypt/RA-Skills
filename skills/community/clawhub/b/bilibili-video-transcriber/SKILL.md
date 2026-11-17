---
name: bilibili-video-transcriber
description: 【B站字幕获取】专业处理 B 站视频字幕问题，支持语音转文字、字幕下载、内容分析。基于实际 B 站字幕系统错误问题开发，提供完整的解决方案。
platforms: [linux, darwin, win32]
commands: [python3, ffmpeg]
---

# 🎬 B 站视频转录专家

**专业处理 B 站视频字幕问题：Wbi签名获取AI字幕 + 三级校验 + 自动降级 + 飞书文档输出**

## ⚡ 快速路径（90%场景用这个）

用户发 B 站链接 → 解析 BV 号 → 跑脚本 → 按结果分支：

```bash
# 短链先解析：curl -sIL "https://b23.tv/xxx" -o /dev/null -w '%{url_effective}' --max-time 20
python3 scripts/bili_subtitle.py BV1xxx   # 技能目录下的脚本
```

| 脚本输出 | 含义 | 下一步 |
|---|---|---|
| ✅ source=player/wbi/v2 | 字幕全量成功 | 直接用 result.json 的 body 写总结 |
| ✅ source=conclusion/get:summary-only | 超长视频无全量字幕，但有官方AI摘要 | 用AI摘要写总结，文档注明摘要级 |
| ❌ 两路径失败 | 无字幕 | 评论课代表 → Whisper（见降级流程） |

输出目录：`/tmp/bili_meta/{bvid}/`（info.json / result.json）

## 🎯 核心根因：AI字幕"张冠李戴"真相（2026-08-09 查明）

**旧结论"CDN缓存key冲突随机返回"是错的。真实根因：缺 Wbi 签名被风控降级。**

- ❌ `/x/player/v2`（无签名）：有时碰巧能用，但被风控降级时返回**随机其他视频的字幕**（HTTP 200 假成功）——这就是历史上"AI字幕张冠李戴"的真相
- ✅ `/x/player/wbi/v2` + Wbi 签名（w_rid/wts）：稳定返回该视频的真实字幕
- 实测：同一视频无签名4次请求首句=LOL解说（错），带签名后4次一致且正确
- 参考：opencli 项目实测"没签名返回200但数据全是空值/降级值"；Bilibili-Evolved #5349 字幕URL错配同款
- **必须校验后才能使用，不能盲信接口返回**

### Wbi 签名算法（脚本已内置）
1. GET `/x/web-interface/nav` → `data.wbi_img` 取 img_key/sub_key（URL末段文件名去扩展名）
2. `mixin_key = 按固定64位乱序表重排(img_key+sub_key)[:32]`
3. 参数加 `wts=当前时间戳` → 按key排序 → 过滤 `!'()*` 字符 → urlencode
4. `w_rid = md5(query + mixin_key)` 追加到参数

### 双路径策略
- **路径1** `/x/player/wbi/v2`：字幕URL列表 → CDN下载 → 校验（CC字幕优先于ai-字幕）
- **路径2** `/x/web-interface/view/conclusion/get`：AI总结接口，返回 summary（全文摘要）+ outline（分节大纲）+ 内置字幕（同样需Wbi签名）
  - ⚠️ 超长视频（>1小时）AI字幕常只生成前几十秒，但 summary 仍完整 → 降级用摘要

### 三级校验（防假数据最后一道闸）
- **strong**：标题关键词（英文≥3字母 + 中文2-4字片段）命中 + 覆盖率≥50%
- **weak**：覆盖率≥70% 且 ≥100句（关键词零命中但覆盖充分，防标题党误杀）
- **fail**：覆盖率<50% / >200% / 关键词零命中且覆盖不足 → 降级

## 📋 完整工作流（脚本内部逻辑，供排障参考）

```python
import requests, json, os

bvid = "BV1xxx"
cookie = open(os.path.expanduser("~/.bilibili_cookie.txt")).read().strip()
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
     "Referer": f"https://www.bilibili.com/video/{bvid}/", "Cookie": cookie}

# 1. 视频信息
d = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}", headers=H, timeout=15).json()["data"]
cid, aid, title, duration, up_mid = d["cid"], d["aid"], d["title"], d["duration"], d["owner"]["mid"]

# 2. Wbi 签名（见上方算法，脚本 get_wbi_keys/enc_wbi 已封装）

# 3. 路径1: 签名字幕列表
params = enc_wbi({"bvid": bvid, "cid": cid}, img_key, sub_key)
j = requests.get("https://api.bilibili.com/x/player/wbi/v2", params=params,
                 headers={**H, "Origin": "https://www.bilibili.com"}, timeout=15).json()
subs = j["data"]["subtitle"]["subtitles"]  # CC字幕(lan无ai-前缀)优先

# 4. 下载字幕并校验（validate 见脚本）
body = requests.get("https:" + sub_url, headers=H, timeout=30).json()["body"]

# 5. 路径2（路径1失败时）: conclusion/get
params = enc_wbi({"bvid": bvid, "cid": cid, "up_mid": up_mid}, img_key, sub_key)
mr = requests.get("https://api.bilibili.com/x/web-interface/view/conclusion/get",
                  params=params, headers=H, timeout=15).json()["data"]["model_result"]
# mr: summary(摘要) / outline(大纲) / subtitle(内置字幕)
```

## 📉 降级流程（脚本两路径都失败时）

```
优先级1: 评论区课代表总结
  GET /x/v2/reply?type=1&oid={aid}&sort=2&pn=1&ps=30
  筛选: 长度>200字 且 点赞>=3 的评论，取最高赞
优先级2: 告知用户"无可用字幕"，询问是否 Whisper 转写（不要擅自下载视频）
优先级3: 用户拒绝下载 → 创建简要文档（视频信息 + 简介 + 概要）
```

## 🎙️ Whisper 转写（无字幕兜底）

```bash
WHISPER="/usr/local/lib/hermes-agent/venv/bin/whisper"
$WHISPER /path/to/audio.wav --model tiny --language zh \
  --output_dir /tmp/output --output_format txt
```

- ⚠️ **不要加 `--fp16 false`**（报 invalid str2bool；CPU自动回退FP32）
- 模型缓存 `~/.cache/whisper/`（已有 tiny/base/medium）；`faster-whisper` 首次调用会联网下模型（网络不通），用本地缓存 CLI
- **先 `uptime` 查负载**：load>4 时 whisper 会极慢/超时，等负载降下来再跑
- CPU 极慢：6分钟音频 tiny 约几分钟，1小时音频约1.5-3小时 → 必须 `background=true` + `notify_on_complete=true`
- 短视频用 tiny；>30分钟或 tiny 乱码用 base；长音频精度优先 base/small
- 低内存服务器（<2GB）：Whisper OOM 时改 Vosk small 分块（180s/块）

### 无字幕视频下载
```python
# 视频直链（无需Cookie，qn=16低清足够转写）
r = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=16&type=mp4&platform=html5",
    headers={"User-Agent": "Mozilla/5.0", "Referer": f"https://www.bilibili.com/video/{bvid}/"}, timeout=15)
video_url = r.json()["data"]["durl"][0]["url"]
```
```bash
curl -sL --max-time 300 -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.bilibili.com/video/{bvid}/" "$VIDEO_URL" -o /tmp/video.mp4
ffmpeg -i video.mp4 -ar 16000 -ac 1 -f wav audio.wav -y
```
⚠️ yt-dlp `--cookies` 不兼容单行 `key=value` 格式（要求 Netscape 格式），直接 curl 直链。

## 🍪 Cookie 管理

```
存储路径（3重冗余）:
  1. ~/.bilibili_cookie_storage
  2. ~/.config/bilibili_transcriber/cookie
  3. ~/.openclaw/workspace/skills/bilibili-video-transcriber/.bilibili_cookie（旧环境存在时）
运行引用: ~/.bilibili_cookie.txt（自动同步，600权限）
```

- 失效检测 + 扫码重登：`bilibili-transcribe --login` / `--check-cookie`（若 CLI 不可用，手动更新 cookie 文件）
- 冗余恢复：活跃文件被删时从备份路径自动恢复
- 飞书扫码流程：生成二维码 → send_qr_via_feishu 写信号文件 → 用户扫码 → poll_login → save_cookie

## 📄 飞书文档输出

### 创建（一步到位带标题）
```bash
cat content.md | lark-cli docs +create --title "[视频总结] UP主 - 标题 - 日期" \
  --wiki-space "{space_id}" --markdown -
# 归类: lark-cli wiki +move --node-token {node_token} --target-parent-token {分类token}
```
- ⚠️ 必须 pipe 传 markdown（`--markdown ./file.md` 会把文件名写进内容，1.0.18 bug）
- ⚠️ wiki/v2/nodes 底层接口无法设标题，必须用 `docs +create`

### 更新已有文档
```bash
# wiki链接先换 obj_token:
lark-cli api GET "/open-apis/wiki/v2/spaces/get_node" --params '{"token":"{node_token}"}'
# 再覆盖更新（mode=overwrite 才是全文替换；replace_all 需要 selection 参数）:
cat new.md | lark-cli docs +update --doc {obj_token} --mode overwrite --markdown -
```

### 权限
- Wiki 文档继承知识库权限，通常无需单独设置
- 需加人时用 Wiki 空间成员 API：`{"member_type":"openid",...}`（**openid 全小写**，open_id 报 131002）
- ❌ 不要用 Drive 权限 API 设 Wiki 文档（报 99992402）
- `lark-cli api --data @file` 必须相对路径

### 知识库选择
| 知识库 | space_id | 场景 |
|---|---|---|
| AI工具 | `7624328764398324948` | AI产品/工具/工作流 |
| 金融财经 | `7623805615265024983` | 股票/投资 |
| 羽毛球AI项目 | `7627078274052558020` | 羽毛球/运动AI |
| 展厅设计 | `7626286573381929940` | 展厅/展会/数字艺术 |
| 具身智能 | `7623664966343609272` | 机器人/多模态 |
| MH扩大疗愈 | `7625549491990432987` | 疗愈理论/实践 |

### 文档结构（必须三部分齐全）
1. 📋 视频信息（lark-table：标题/UP主/时长/链接/数据）
2. 📝 结构化内容总结 + 🔑 核心要点（**不是字幕复制粘贴**；用户要求详细、写出核心要点）
3. 📄 原文备查链接（B站视频链接）

Markdown 格式：表格用 `<lark-table>`、高亮用 `<callout emoji="🎬" background-color="light-blue">`、内容中不写一级标题（title 参数已设）。

## ⚠️ 关键规则

### 用户发 B 站链接的强制流程
1. 收到链接 → 加载本技能 → 跑 `scripts/bili_subtitle.py`
2. 不能跳过技能直接 raw requests 调无签名接口（历史教训：2026-06-02 WBI签名不完整导致字幕列表为空）
3. 校验失败/无字幕 → 按降级流程，Whisper 前**先征得用户同意**

### 输出目录命名（必须带标识）
```
/tmp/{UP主}_{视频标题}_{BV号}/   ← 唯一标识三元组
├── bili_subs.json / summary.md / comments.json
```
❌ 禁止 `/tmp/bili_subs.json` 这种无标识名（会互相覆盖）。特殊字符去掉 `/ \ : * ? " < > |`。

### 进度通知（飞书 interim 消息关闭）
- 收到链接先告知预计耗时（字幕1-3分钟 / Whisper 15分钟-3小时）
- API响应慢≠卡死，不要擅自取消；超10分钟无输出才主动报进度

### 评论获取
```python
requests.get(f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=2&pn=1&ps=20", headers=H, timeout=15)
```

## 🔧 故障排除

| 症状 | 原因 | 解决 |
|---|---|---|
| 字幕内容张冠李戴 | 无Wbi签名被风控降级 | 必须走 bili_subtitle.py（签名版） |
| wbi/v2 返回 code=-403/空 | w_rid 算错/wts过期 | 重新取 nav 的 img_key/sub_key，时间戳用当前 |
| conclusion 接口 summary 为空 | 视频无AI总结（旧视频/短视频） | 正常，走路径1或降级 |
| 超长视频字幕只覆盖前几十秒 | B站对长视频AI字幕固有限制 | 用 conclusion summary 写摘要级文档，或Whisper |
| `bilibili_api` pip 装不上 | pyyaml build 失败 | 不用它，全程 raw requests |
| `Credential() unexpected keyword` | bilibili_api 9.x 参数变更 | 不用 bilibili_transcriber.py 模块 |
| whisper 超时 | 服务器负载高 | uptime 查负载，降下来再跑/转后台 |
| OOM（<2GB内存） | whisper 内存不足 | Vosk small 分块（180s/块） |

## 📎 参考文件
- `references/series-discovery.md`：系列视频发现方法与处理策略
- `references/feishu-wiki-api.md`：飞书Wiki API细节

---

**更新记录：**
- 2026-08-09：🔥 重大重写。查明AI字幕张冠李戴真因=缺Wbi签名被风控降级（推翻CDN缓存旧结论）；新增 scripts/bili_subtitle.py（Wbi签名+player/wbi/v2+conclusion/get双路径+三级校验）；超长视频摘要降级路径；docs +update overwrite 用法；结构重组
- 2026-07-19：系列视频发现方法、超长有字幕视频策略
- 历史：评论获取、Cookie冗余存储、Vosk分块、输出目录命名、yt-dlp不兼容等（见上方各节）
