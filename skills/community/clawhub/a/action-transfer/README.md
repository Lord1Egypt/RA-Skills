# 动作迁移 Skill

让你的角色做参考视频里的动作。基于参考图片和输入视频生成动作迁移后的视频结果。

> **零安装**：本 Skill 自带的客户端只用 Python 标准库，不用 pip、不用 GPU、不用配环境。
> 你只需要一把 **api.a7w.cn 的 API Key**，然后把两个公网地址传进来就行。

---

## 30 秒上手

```bash
# 1. 配一次 Key（去 https://api.a7w.cn/ 注册即可领取）
python3 scripts/client.py login --key sk-你的key

# 2. 提交任务：一张人物图 + 一段视频，两个都要公网可访问的地址
python3 scripts/client.py call action_transfer submit \
    --param file_url="https://你的图床/人物.png" \
    --param video_url="https://你的图床/素材.mp4" \
    --param mode=fast

# 3. 等它就绪（脚本会自动轮询到出片，直接给你视频地址）
```

**实测跑通的样子**（4 秒素材 / fast 档）：

```
task_id = task_3385aedd6ec41a5f97f7aee2（预计消耗 4.46 点）
  状态：processing
  状态：completed
{"ok": true, "video_url": "https://oss.gpu.likeadmin.cn/server/video_transfer/...mp4"}
```

| | |
|---|---|
| **输入** | 一张人物照 + 一段 4 秒动作视频 |
| **产出** | 4 秒成片（480×864 / 15fps），标准 MP4 |
| **耗时** | 约 3 分钟 |
| **花费** | 4.46 点（fast 档 1 点/秒；standard 2 点/秒；max 3 点/秒） |

---

## ⚠️ 两个地址必须是公网可访问的 URL

这是最容易卡住的地方——**本地文件传不进去**。先让它变成公网地址：

- **图床**：任意图床都行，拿到 `https://` 直链即可
- **对象存储**：阿里云 OSS / 腾讯云 COS / 七牛，开公共读
- **临时直链**：`0x0.st`、`transfer.sh`、`tmpfiles.org` 这类临时文件服务
- **自己有服务器**：丢到静态目录，直接用 `https://你的域名/文件.mp4`

> **还有个坑**：不是所有公网地址平台都抓得动。实测 `download.samplelib.com` 的样片会返回
> `502 upstream timeout`，换一个来源就好了。如果报 502，先换地址重试。

---

## 目录结构

```
action-transfer/
├── SKILL.md                   概览、接口索引与参数表
├── README.md                  本文件
├── LICENSE.md
├── references/
│   ├── getting-started.md     注册 / 充值 / 取 Key / 配置
│   └── api-*.md               各接口官方文档（2 个）
└── scripts/
    └── client.py                 通用客户端（零依赖）
```

---

## 客户端命令

| 命令 | 作用 |
|---|---|
| `login --key sk-xxx` | 验证并保存 Key 到 `~/.a7w/config.json` |
| `whoami` | 验证 Key，看可用插件数 |
| `apps` | 列出这个 Key 能用的所有插件 |
| `schema <app>` | 看某插件的接口与参数 |
| `call <app> <api> --json '{...}'` | 调用接口（异步自动轮询） |
| `task <task_id>` | 查异步任务状态 |
| `points` | 看最近任务的用量汇总 |

`--key` / `--host` 放在子命令前后都可以。

---

## 依赖

- Python 3.8+，**仅标准库**（urllib），无第三方包
- 需要能访问 `api.a7w.cn`

---

## 安全

- Key 存在本机 `~/.a7w/config.json`（权限 600）或环境变量 `A7W_API_KEY`
- 脚本只把 Key 发往 `api.a7w.cn`
- **不要**把 Key 提交到代码仓库

---

## 许可证

MIT，见 `LICENSE.md`。

---

---

## 联系我们

- **技术微信：9872659** —— 加好友时说一下是从哪个 Skill 找过来的，直接给你配套的 API Key 与能跑的示例。
- **要算力 / 要 API Key**：[算力集市 · 注册领 API Key](https://api.a7w.cn/) —— 一个 Key 调用全部 AI 算力，注册、充值、创建 Key 都在这里。
- **更多 AI 插件与接口**：[AI 插件市场](https://aigc.a7w.cn/)。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 浏览全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |
| [0人公司 · AI Agent 平台](https://a7w.cn/) | a7w.cn | 主站，了解整套 AI Agent 生态 |
