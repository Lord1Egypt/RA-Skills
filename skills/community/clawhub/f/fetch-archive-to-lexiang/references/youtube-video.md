#### YouTube / 嵌入视频处理（yt-dlp + Whisper + 翻译 + 乐享）

**适用场景**：
- 用户直接提供 YouTube 视频链接
- 用户提供含嵌入视频/播客的页面（Substack、Newsletter 等），需先用 WebFetch 提取页面中的 YouTube 链接

**⚠️ 重要**：**不要**使用 `web_fetch`（无法获取视频内容），**不要**使用 NotebookLM（已替换为本地 Whisper 方案，速度更快、无外部依赖）。

**工作流概述**：
1. **（可选）从页面提取 YouTube 链接** — 用 WebFetch 抓取页面，提取 `youtu.be/xxx` 或 `youtube.com/watch?v=xxx`
2. **yt-dlp 下载视频** → 本地 `.mp4` 文件
3. **ffmpeg 提取音频** → WAV 格式（16kHz 单声道）
4. **Whisper 转录** → 带时间戳的文字稿
5. **AI 翻译**（如果是英文）→ 中英对照格式的 Markdown
6. **上传乐享知识库**（标题文件夹结构 — 文字稿为主文档，视频为子文档）：
   - a. 创建日期目录（如已存在则复用）
   - b. 在日期目录下创建**以标题命名的文件夹**
   - c. 上传**文字稿**为 file entry（预签名 URL 三步），放在标题文件夹内
   - d. 上传**原视频文件**到同一标题文件夹内（VOD 路径，作为子文档）
7. **清理**：上传成功后删除本地视频和音频文件

**🚨 乐享目录结构（关键变更）**：

```
贾维斯知识库/
└── 2026-06-03/                        ← 日期目录
    └── A rational conversation...     ← 标题文件夹
        ├── 文字稿.md（file entry）     ← 主内容：转录+翻译（预签名 URL 上传）
        └── 视频.mp4（video entry）      ← 原始视频文件（VOD 路径上传）
```

这样组织的好处：
- 文字稿和视频逻辑上绑定在一起
- .md 文件支持全文搜索和预览
- 视频作为附属文件，在乐享中可直接播放
- 播客音频同理：标题文件夹 > 文字稿.md + 音频.m4a

**Step 1：下载 + 转录 + 翻译**

```bash
cd <项目子目录>

# 完整流程（下载 + 转录 + 翻译）
python3 scripts/yt_download_transcribe.py "<YouTube URL>" \
  --output-dir . \
  --whisper-model base

# 常用参数：
#   --whisper-model tiny|base|small|medium|large  转录模型（越大越准但越慢）
#   --skip-download    跳过下载（用于重新转录已下载的视频）
#   --skip-translate   跳过翻译步骤
#   --keep-audio       保留提取的音频文件
```

**产出物**：
- `<视频标题>.mp4` — 下载的视频文件
- `<视频标题>.md` — 文字稿 Markdown（英文视频为中英对照格式）
- `<视频标题>_meta.json` — 视频元信息

**文字稿格式**（含视频介绍 + 逐字稿）：

```markdown
# 视频标题

**频道**: xxx
**发布日期**: 2026-03-10
**时长**: 15:30
**原始链接**: https://www.youtube.com/watch?v=xxx
**转录语言**: en

---

## 视频介绍

（YouTube description / Show Notes，yt-dlp 自动提取）

---

## 逐字稿（中英对照）

> 以下内容采用「英文原文 + 中文翻译」对照排列。

**[00:00]**

This is the original English text from the video...

这是视频中的中文翻译文本...

**[01:23]**

Next paragraph of English text...

下一段中文翻译...
```

**Whisper 模型选择建议**：

| 模型 | 速度 | 精度 | 适用场景 |
|------|------|------|---------|
| `tiny` | 最快 | 较低 | 快速预览、非关键内容 |
| `base` | 快 | 中等 | **默认推荐**，适合大部分场景 |
| `small` | 中等 | 较高 | 口音较重、背景噪音较多 |
| `medium` | 慢 | 高 | 重要内容、需要高精度 |
| `large` | 最慢 | 最高 | 专业内容、学术演讲 |

**Step 2：上传到乐享知识库（文字稿 + 视频子文档）**

> 通过 lexiang MCP 工具 + OpenAPI 脚本完成上传。**前提是 lexiang MCP 已连接**。

**完整上传流程**：

```
1. 获取知识库根节点 → 检查/创建日期目录
2. 在日期目录下创建「标题文件夹」
3. 上传文字稿到标题文件夹（在线文档 page）
4. 上传视频到标题文件夹（video entry，作为子文档）
```

**步骤 2a：创建标题文件夹**：
```
entry_create_entry(entry_type="folder", parent_entry_id=<日期目录ID>, name="<视频标题>")
```

**步骤 2b：上传文字稿**（在线文档 page 类型）：
- 纯文本 ≤30K 字符：`entry_import_content(space_id, parent_id=<标题文件夹ID>, name="<视频标题>", content=<md内容>, content_type="markdown")`
- 纯文本 >30K 字符：`scripts/upload_doc_to_lexiang.py <文件.md> --parent-id <标题文件夹ID> --name "标题" --space-id <SPACE_ID>`
- 在线文档支持后续在乐享中按块维度编辑更新（如修正翻译）

**步骤 2c：上传视频文件**（🚨 必须用 OpenAPI，不用 MCP `file_apply_upload`）：

```bash
# ✅ 推荐：通过 OpenAPI 上传，产生 entry_type=video，乐享会 VOD 转码，真能播放
python3 scripts/upload_video_via_openapi.py "<视频路径>.mp4" \
    --space-id <space_id> \
    --parent-entry-id <标题文件夹 entry_id> \
    --media-type video
```

视频作为子文档放在标题文件夹下，与文字稿并列。

需要在 `~/.lexiang/openapi.json` 配置 AppKey/AppSecret/StaffID（**不入 git**）。

OpenAPI 正确流程（脚本已封装）：
1. `POST /cgi-bin/v1/kb/files/upload-params`（body: `{"name":"xxx.mp4","media_type":"video"}`）→ 获取 VOD 上传签名 + state
2. `PUT <bucket>.cos.<region>.myqcloud.com/<key>` → 上传到 VOD COS
3. `POST /cgi-bin/v1/kb/entries?space_id=xxx&state=xxx`（body: `entry_type=video, name=xxx.mp4`）→ 创建可播放视频节点

**🚨 关键踩坑（2026-05-03 实战总结）**：
- ❌ 不要用 MCP 的 `file_apply_upload`——产物是 `entry_type=file + extension=video`，不触发 VOD 转码，**视频无法播放**
- ❌ 不要用 `/cgi-bin/v1/docs/cos-param` 签名接口——它只支持 `attachment/file`，签发的 state 不能用于创建 entry_type=video
- ✅ **必须用 `/cgi-bin/v1/kb/files/upload-params`**——支持 `media_type=video/audio/file`，签发的 state 可用于 `kb/entries`
- ✅ `name` 参数**必须带文件后缀**（`.mp4` 等），否则报"name 需指定文件后缀"
- ✅ `kb/entries` 接口用 **`x-staff-id`**（小写带连字符），不是 `StaffID`

**备用：MCP 三步流程（仅适用于非视频文件，如 PDF）**：
1. `file_apply_upload`（参数：`parent_entry_id=<日期目录ID>`, `name="<文件名>.pdf"`, `size=<文件字节数>`, `mime_type="application/pdf"`, `upload_type="PRE_SIGNED_URL"`）
2. `curl -X PUT "<upload_url>" -H "Content-Type: application/pdf" --data-binary "@<文件路径>"`
3. `file_commit_upload`（参数：`session_id=<上一步返回的session_id>`）

**上传成功后**：自动删除本地视频文件（`rm -f <视频文件路径>`），节省磁盘空间。

**依赖**：
- `yt-dlp`（**推荐 `brew install yt-dlp`**，不要用 `pip3 install`）— YouTube 视频下载。必须用 brew 安装以获取最新版本，pip 版本受限于系统 Python 版本（如 Python 3.9 无法安装 nightly 版），而 brew 版自带独立 Python 环境
- `openai-whisper`（`pip3 install openai-whisper`）— 音频转录
- `ffmpeg`（`brew install ffmpeg`）— 音频提取
- `openai`（`pip3 install openai`）— 翻译（需要 `OPENAI_API_KEY` 环境变量）。**如果没有 API Key，可以跳过翻译步骤，由 AI 助手直接在对话中翻译后更新文档**

**🚨 沙箱环境 Whisper 执行策略（与播客音频相同，禁止静默降级）**：

YouTube 视频的 Whisper 转录同样依赖 `torch`，在沙箱环境可能遇到 code signing 错误。处理流程同播客音频：
1. 先尝试沙箱内执行
2. 如遇 code signing 错误 → 向用户说明并申请 `dangerouslyDisableSandbox: true` 权限
3. 仅当用户明确拒绝时才可降级（如使用 YouTube 自带字幕替代 Whisper 转录）

