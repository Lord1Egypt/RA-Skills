# fetch-archive-to-lexiang

通用 AI Agent Skill：抓取文章 / 视频 / 播客 / PDF 论文，并归档到[乐享](https://lexiangla.com)知识库。

适用于 [WorkBuddy](https://www.codebuddy.cn/docs/workbuddy/Overview)、[QClaw](https://qclaw.qq.com)、[CodeBuddy](https://www.codebuddy.ai/)、[OpenClaw](https://openclaw.ai/)、[Claude Code](https://docs.anthropic.com/en/docs/claude-code)、[Gemini CLI](https://github.com/google-gemini/gemini-cli) 等所有支持 Skill / Custom Instructions 机制的 AI Agent。

## 功能概述

将任意 URL 的内容抓取为结构化 Markdown，自动转存到乐享知识库，实现素材归档和可追溯。

### 支持的内容类型

| 类型 | 来源 | 处理方式 |
|------|------|---------|
| 📝 **图文文章** | 微信公众号、Substack、Medium、知识星球等 | Playwright 抓取 → Markdown + 图片 → 上传乐享 |
| 🔒 **付费/登录墙文章** | Substack 付费订阅、Medium 会员等 | Chrome Cookie 注入 / CDP 模式 → 全文抓取 |
| 🎬 **YouTube 视频** | YouTube、Substack/Newsletter 嵌入视频 | yt-dlp 下载 → Whisper 转录 → AI 翻译（中英对照）→ 标题文件夹归档 |
| 🎙️ **播客音频** | 小宇宙FM、Apple Podcasts 等 | yt-dlp 下载音频 → FunASR/Whisper 转录 → 标题文件夹归档 |
| 📄 **免费文章** | 任意公开网页 | web_fetch / Playwright → Markdown → 上传乐享 |
| 📑 **PDF 文件/论文** | arXiv、乐享知识库已存 PDF、本地文件等 | 组合 **`pdf-rich-translate`** skill 做提取/裁剪/翻译/富元素标注 → 本 skill 归档（导入 + 标注渲染成 callout/表格块） |

### 乐享知识库归档

- 按**天维度**自动创建日期目录（如 `2026-06-03/`），新建后置于目录顶部
- **视频/播客转录**：采用「标题文件夹」结构 — 日期目录下创建以标题命名的文件夹，文字稿和媒体文件并列存放
- 图文文章通过 MCP connector 上传（先全文后补图），保留原始图片
- 大文档（>30K字符）通过预签名 URL 三步上传，绕过 MCP 参数限制
- 自动**去重检查**，避免重复上传
- 通过 **lexiang MCP** 工具操作知识库，安全且通用
- 输出的乐享文档链接格式：`https://lexiangla.com/pages/{entry_id}?company_from={company_from}`

### 视频/播客归档目录结构

```
贾维斯知识库/
└── 2026-06-03/                              ← 日期目录（自动置顶）
    ├── A Rational Conversation... - Benedict Evans/  ← 标题文件夹
    │   ├── 文字稿.md（file entry）           ← 转录+翻译（预签名URL上传）
    │   └── 视频.mp4（video entry）            ← 原始视频（VOD路径上传）
    └── 某期播客标题/                          ← 标题文件夹
        ├── 文字稿.md（file entry）            ← 转录文字稿
        └── 音频.m4a（audio entry）            ← 原始音频（VOD路径上传）
```

### PDF 处理（已拆分为独立 skill）

PDF 的「图文提取 + 富元素识别 + 中英对照翻译 + 可移植排版」已抽离为独立 skill **`pdf-rich-translate`**（项目 `.cursor/skills/`）。两者**组合使用**：

- `pdf-rich-translate`：PDF → 可移植双语 markdown 包（正文 + `images/` + `> [!stat]`/`> [!definition]` 标注 + HTML 表）。
- 本 skill（归档侧）：导入乐享、三步传图、把标注渲染成 callout/原生表格块、转存后增量改块、md↔线上对账。详见 [references/pdf-processing.md](references/pdf-processing.md)。

## 文件结构

```
fetch-archive-to-lexiang/
├── SKILL.md                      # Skill 定义文件（Agent 指令）
├── config.json.example           # 配置模板（首次使用时复制为 config.json）
├── README.md                     # 本文件
├── scripts/
│   ├── fetch_article.py          # 文章抓取脚本（Cookie 注入 / CDP 模式）
│   ├── md_to_page.py             # Markdown → 乐享在线文档（含图片上传和置顶）
│   ├── md_to_pdf.py              # Markdown → PDF 转换（嵌入图片、中文渲染）
│   ├── translate_gemini.py       # 文章翻译（Gemini API）
│   ├── upload_doc_to_lexiang.py  # 大文档上传（绕过 MCP 参数限制）
│   ├── upload_video_via_openapi.py # 视频/音频上传（走 OpenAPI VOD 路径）
│   ├── podcast_to_lexiang.py     # 播客全流程（下载→FunASR转录→Markdown）
│   └── yt_download_transcribe.py # YouTube 下载 + Whisper 转录 + AI 翻译
├── references/                   # 按需加载的详细参考文档
│   ├── lexiang-upload.md         # 乐享上传详细步骤和降级方案
│   ├── youtube-video.md          # YouTube/嵌入视频处理流程
│   ├── podcast-audio.md          # 播客音频处理流程
│   ├── pdf-processing.md         # PDF 归档侧（提取/翻译见 pdf-rich-translate skill）
│   ├── platform-specific.md      # 微信/得到/SPA/Substack/X/微博等特定平台
│   ├── tips-experience.md        # 经验总结
│   └── troubleshooting.md        # 常见问题排查
└── tests/                        # 回归测试用例
    └── test-cases.json           # 测试场景定义
```

## 安装

只需在 Agent 对话中发送：

```
帮我安装这个 skill：https://github.com/ajaxhe/fetch-archive-to-lexiang
```

Agent 会自动完成仓库克隆、依赖安装和初始配置。

### 前置条件

1. **乐享 MCP**：本 Skill 通过 [lexiang MCP](https://github.com/nicognaW/lexiang-mcp) 操作乐享知识库，需提前在 Agent 的 MCP 配置中添加 lexiang server（[获取 Token](https://lexiangla.com/mcp)）
2. **Python 3.8+**：脚本运行环境
3. **pymupdf**（PDF 处理）：`pip install pymupdf`

> 其他依赖（Playwright、yt-dlp、Whisper 等）均由 Agent 在首次使用时自动检测并安装，无需手动操作。

## 使用方式

在 Agent 对话中直接使用自然语言：

```
# 抓取微信公众号文章并归档
把这篇文章转存到知识库：https://mp.weixin.qq.com/s/xxxxx

# 抓取 Substack 付费文章
抓取这篇文章：https://www.lennysnewsletter.com/p/xxxxx

# YouTube 视频转录（含嵌入视频的页面也支持）
转录这个视频：https://www.youtube.com/watch?v=xxxxx

# 播客转录
转录这期播客：https://www.xiaoyuzhoufm.com/episode/xxxxx

# PDF 论文翻译转存（arXiv 直链）
把这篇论文转存到乐享知识库：https://arxiv.org/pdf/2605.05538

# PDF 论文翻译转存（乐享已存 PDF）
把乐享里的这篇论文翻译转存：https://lexiangla.com/pages/xxxxx?company_from=yyyyy
```

## 脚本独立使用

脚本也可以脱离 Skill 框架独立运行：

```bash
# 抓取文章（Cookie 注入模式）
python3 scripts/fetch_article.py fetch <URL> --output-dir <输出目录>

# 抓取文章（CDP 模式，适用于 Substack/微博等需要完整登录态的站点）
python3 scripts/fetch_article.py fetch <URL> --output-dir <输出目录> --cdp

# Substack 登录（首次使用前执行一次）
python3 scripts/fetch_article.py login

# Markdown 转乐享在线文档（自动置顶）
python3 scripts/md_to_page.py <article.md路径> --parent-id <父目录ID> --name "文章标题"

# 大文档上传乐享（绕过 MCP 参数限制）
python3 scripts/upload_doc_to_lexiang.py <文件.md> --parent-id <目录ID> --name "标题" --space-id <SPACE_ID>

# YouTube 视频下载 + 转录 + 翻译
python3 scripts/yt_download_transcribe.py <YouTube URL> --output-dir <输出目录>

# 播客全流程转录
python3 scripts/podcast_to_lexiang.py <播客URL> --output-dir <输出目录> --language zh

# 视频/音频上传乐享（VOD 路径）
python3 scripts/upload_video_via_openapi.py <文件.mp4> --space-id <SPACE_ID> --parent-entry-id <目录ID> --media-type video
```

## 配置说明

首次使用时将 `config.json.example` 复制为 `config.json`，Skill 会在对话中引导完成配置，也可手动编辑：

```bash
cp config.json.example config.json
```

```json
{
  "_initialized": true,
  "lexiang": {
    "target_space": {
      "space_id": "<知识库ID>",
      "space_name": "<知识库名称>",
      "company_from": "<企业标识>"
    },
    "access_domain": {
      "domain": "lexiangla.com",
      "page_url_template": "https://lexiangla.com/pages/{entry_id}?company_from={company_from}",
      "space_url_template": "https://lexiangla.com/spaces/{space_id}?company_from={company_from}"
    }
  }
}
```

> ⚠️ `config.json` 包含你的私有知识库信息，已被 `.gitignore` 忽略，不会被提交到仓库。

## 最近更新 (2026-06-03)

### v2.1 — 视频/播客「标题文件夹」归档结构

- **新增**：视频和播客转录归档采用「标题文件夹」结构 — 日期目录下创建以标题命名的文件夹，文字稿(.md)和媒体文件并列存放
- **新增**：支持从 Substack/Newsletter 页面自动提取嵌入的 YouTube 链接进行转录
- **新增**：Gemini 2.5 Flash 分批翻译（中英对照格式），支持补翻失败段落
- **新增**：大文档通过预签名 URL 三步上传（file_apply_upload → PUT → file_commit_upload）
- **新增**：文件更新/重新上传支持（describe_entry 获取 file_id → apply_upload with file_id）
- **新增**：`tests/` 目录存放回归测试用例
- **优化**：播客音频归档方式与视频统一（标题文件夹结构）
- **修复**：Whisper 转录时文件名含特殊字符导致 ffmpeg 失败
- **修复**：代理间歇断开导致 Gemini 翻译失败（env -u 清除代理）

## 已知行为注意事项

- **乐享文档链接**：必须带 `?company_from=xxx` 参数，否则无法访问。`mcp.lexiang-app.com` 格式为 MCP 内部调试链接，用户不可访问。
- **entry_move_entry 置顶**：`after=""` 实测是移到末尾（与接口文档描述相反）。正确置顶方式：先查父目录第一个条目 ID，用 `before=<该ID>` 排在其前。
- **entry_import_content 不支持位置控制**：用此接口创建的文档永远追加到目录末尾，无法通过参数控制顺序，需创建后调用 `entry_move_entry` 调整。
- **PDF 矢量图**：流程图、柱状图等矢量图无法用 `extract_image()` 提取，必须用 `get_pixmap(clip=Rect(...))` 截取指定区域。
- **视频/音频上传**：必须走 OpenAPI VOD 路径（`upload_video_via_openapi.py`），MCP 的 `file_apply_upload` 产生不可播放的 file 条目。
- **大文档（>30K字符）**：禁止通过 MCP 工具参数直接传入，必须用预签名 URL 三步上传。

## 兼容性

| Agent | 支持方式 | 说明 |
|-------|---------|------|
| **WorkBuddy** | `~/.workbuddy/skills/` | 原生 Skill 目录，自动加载 |
| **QClaw** | `.qclaw/skills/` | 原生 Skill 目录，自动加载 |
| **CodeBuddy** | `.codebuddy/skills/` | 原生 Skill 目录，自动加载 |
| **OpenClaw** | `.claude/skills/` | 通过 Custom Instructions 加载 SKILL.md |
| **Claude Code** | `.claude/skills/` | 同 OpenClaw |
| **Gemini CLI** | `.gemini/skills/` | 通过 Custom Instructions 加载 SKILL.md |
| **其他 Agent** | 手动加载 | 将 SKILL.md 内容作为 System Prompt 传入即可 |

## License

MIT
