# 🎬 bilibili-video-transcriber

**B 站视频转录专家** —— AI Agent 技能：获取 B 站视频字幕、语音转文字、内容总结，并输出结构化飞书文档。

> v3.0.0 重大更新：查明 AI 字幕"张冠李戴"真因（缺 Wbi 签名被风控降级），新增带签名 + 三级校验的字幕获取脚本，长视频自动降级官方 AI 摘要。

## ✨ 核心特性

- 🔐 **Wbi 签名字幕获取**：`/x/player/wbi/v2` 带完整签名，杜绝风控降级返回的随机假字幕
- 🧩 **双路径容错**：player/wbi/v2 失败 → conclusion/get（AI 总结接口内置字幕 + 全文摘要）
- 🛡️ **三级内容校验**：strong（标题关键词命中）/ weak（覆盖率≥70%）/ fail（拒绝并降级）
- 📉 **智能降级链**：CC字幕 → AI字幕 → 官方AI摘要 → 评论课代表 → Whisper 转写
- 🎙️ **低资源转写**：Whisper CLI（先查负载）+ Vosk 分块（<2GB 内存服务器）
- 🍪 **Cookie 管理**：3 重冗余存储 + 失效检测 + 飞书扫码重登
- 📄 **飞书文档输出**：一步创建带标题 Wiki 文档 + 知识库自动归类

## 🚀 快速开始

```bash
# 安装（ClawHub）
clawhub install bilibili-video-transcriber

# 获取字幕（核心命令）
python3 scripts/bili_subtitle.py BV1xxx
```

输出 `/tmp/bili_meta/{bvid}/result.json`，按结果分支：

| 输出 | 含义 | 下一步 |
|---|---|---|
| `source=player/wbi/v2:*` | 字幕全量成功 | 用 body 写总结 |
| `source=conclusion/get:summary-only` | 超长视频无全量字幕，有官方摘要 | 用摘要写总结 |
| 两路径失败 | 无字幕 | 评论课代表 → Whisper |

## 🔍 为什么需要 Wbi 签名（v3.0 核心修复）

**历史现象**：AI 字幕"张冠李戴"——拿到的字幕内容属于别的视频。

**旧诊断（错误）**：CDN 缓存 key 冲突随机返回。

**真实根因（2026-08-09 实测查明）**：
- ❌ `/x/player/v2`（无签名）：有时碰巧可用，但被风控降级时返回**随机其他视频的字幕**（HTTP 200 假成功）
- ✅ `/x/player/wbi/v2` + Wbi 签名：稳定返回该视频真实字幕
- 实测对照：同一视频无签名 4 次请求首句=LOL解说（错），带签名后 4 次一致且正确

**Wbi 签名算法**：
1. GET `/x/web-interface/nav` → 取 `img_key` / `sub_key`
2. 按固定 64 位乱序表重排 `(img_key + sub_key)` 取前 32 位 = `mixin_key`
3. 参数加 `wts=时间戳` → 按 key 排序 → 过滤 `!'()*` → urlencode
4. `w_rid = md5(query + mixin_key)`

## 📦 目录结构

```
├── SKILL.md                    # 技能主文档（Agent 执行手册）
├── scripts/
│   └── bili_subtitle.py        # ⭐ v3.0 核心：Wbi签名+双路径+三级校验
├── references/
│   ├── series-discovery.md     # 系列视频发现方法
│   └── feishu-wiki-api.md      # 飞书 Wiki API 细节
├── bilibili_transcriber.py     # 旧版模块（不推荐直接用，见 SKILL.md 故障表）
├── cookie_manager.py           # Cookie 冗余存储/扫码登录
├── cli.py                      # bilibili-transcribe CLI
├── examples/                   # 使用示例
└── package.json                # 版本与 changelog
```

## 📉 降级流程

```
优先级1: UP主CC字幕（lan 无 ai- 前缀）
优先级2: B站AI字幕（带签名获取 + 校验）
优先级3: conclusion/get 官方AI摘要（超长视频兜底）
优先级4: 评论区课代表总结（长度>200字 且 点赞>=3）
优先级5: Whisper 转写（需用户同意下载视频；先 uptime 查负载）
```

## ⚠️ 已知限制

- **超长视频**（>1小时）：B 站 AI 字幕常只生成前几十秒（平台固有限制），此时用 conclusion/get 的官方摘要写摘要级文档，或 Whisper 全量转写
- **bilibili-api pip 包**：pyyaml build 常失败且 9.x 接口不兼容，本技能全程 raw requests，不依赖它
- **yt-dlp**：`--cookies` 不兼容单行 cookie 格式，用 playurl + curl 直链下载

## 📄 飞书文档输出

技能内置飞书工作流（lark-cli）：
- `docs +create --title --wiki-space --markdown -`（pipe 传内容，避免文件名 bug）
- `docs +update --mode overwrite`（全文覆盖更新）
- Wiki 空间成员 API 授权（`member_type: "openid"` 全小写）

## 📝 Changelog

### v3.0.0 (2026-08-09)
- 🔥 查明 AI 字幕张冠李戴真因 = 缺 Wbi 签名被风控降级（推翻 CDN 缓存旧结论）
- 🔐 新增 `scripts/bili_subtitle.py`（Wbi签名 + 双路径 + 三级校验）
- 🧩 超长视频自动降级官方 AI 摘要
- 📖 SKILL.md 全面重写

### v2.4.0
- 删除视频转录冗余步骤，优化超 30 分钟用户确认逻辑；faster-whisper 按需安装

### v2.1.0
- 💬 热门评论获取（按点赞排序 + 回复）

### v2.0.0
- 🚀 智能优先级处理（CC→AI→音频→下载），性能提升 96%
- 🧠 系统资源检测 + Vosk 离线引擎 + 扫码登录

## 🔗 链接

- GitHub: https://github.com/adolescen-he/bilibili-video-transcriber
- ClawHub: `clawhub install bilibili-video-transcriber`
- Issues: https://github.com/adolescen-he/bilibili-video-transcriber/issues

## 📞 License

MIT
