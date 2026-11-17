---
name: fetch-archive-to-lexiang
version: "4.1.0"
author: ajaxhe
license: MIT
category: research
description: Discover and fetch articles, videos, podcasts, and PDFs into standardized source packages, then orchestrate deduplicated Lexiang archival. 侦察和抓取文章、视频、播客与 PDF，生成标准来源工作包并编排乐享归档。
tags: fetch, archive, youtube, podcast, pdf, transcribe, lexiang, paywall, substack, medium, arxiv
disable-model-invocation: false
requires:
  skills:
    - name: trans-doc-to-md
      version: ">=3.0.0,<4.0.0"
    - name: upload-markdown-to-lexiang
      version: ">=1.1.0,<2.0.0"
  binaries:
    - python3
    - yt-dlp
  python:
    - playwright
    - pymupdf
    - openai-whisper
---

# 抓取来源并编排乐享归档

本 Skill 只负责：

1. 来源侦察和抓取方式选择。
2. 网页抓取、视频/播客下载与转录。
3. 生成统一工作包。
4. 乐享目录、去重和视频/音频 VOD 编排。

本 Skill 不负责：

- 非中文 Markdown 的清洗、翻译和完整性验证：统一委托
  `trans-doc-to-md` 的 **Prepared Markdown Package** 模式。
- 任何 Markdown 页面写入：统一委托 `upload-markdown-to-lexiang`。
- 在上传后用 MCP 二次渲染正常富元素：uploader 直接渲染
  `trans-doc-to-md` 标注。

## 强制边界

1. `source.md` 是不可变原文；若同目录已有不同内容，必须换工作目录，禁止覆盖。
2. 禁止摘要替代原文，禁止丢失图片、Show Notes 或转录内容。
3. 最终 Markdown 文件名必须是原文标题；文件名非法字符可安全替换，但 `meta.json`
   中的 `title` 和 `source_title` 必须保留原始标题。
4. 中文来源可由编排流程把 `source.md` 复制为 `<原文标题>.md`；抓取脚本不自行决定。
5. 非中文来源必须先交给 `trans-doc-to-md`，不得在本 Skill 或当前 Agent
   内实现翻译。
6. Markdown 页面只用 uploader 写入，不得恢复任何旧导入、文件上传或本地上传器副本。
7. 视频和音频继续使用 `scripts/upload_video_via_openapi.py` 的 VOD 路径。
8. 上传后少量人工增量修复仅是异常维护路径；每次修复必须同步本地最终 Markdown。

## 统一工作包

```text
<work-dir>/
├── source.md               # 不可变原文
├── images/                 # 可选，引用路径保持相对
├── meta.json
└── <原文标题>.md           # 编排完成后的最终 Markdown
```

`meta.json` 标准字段：

```json
{
  "title": "归档标题",
  "source_url": "https://...",
  "source_title": "原文标题",
  "source_type": "article|youtube|podcast|pdf",
  "language": "zh|en|...",
  "parent_id": "可选的目标目录 ID"
}
```

允许保留作者、日期、时长、媒体文件等扩展字段。

## Step 0：预检与来源侦察

1. 阅读 `references/lessons-learned.md` 中全部 P0 教训。
2. 侦察标题、作者、日期、语言、长度、图片数、媒体时长、付费墙和登录墙。
3. 有图片必须用抓取脚本下载，不能只依赖 WebFetch。
4. 网页抓取默认使用 CDP：先检查已配置端口（默认 9222，实际端口记录在
   `~/.fetch_article/cdp_port`）和有效 page target，复用已有浏览器上下文与登录态，
   并在其中新开任务标签页；端口未启动时主动启动 CDP Chrome。CDP 连接失败
   必须退出，禁止静默回退到无登录态的 Testing Chrome。只有用户明确要求隔离浏览器时
   才使用 `--no-cdp`。
5. 确定新的独立工作目录，避免覆盖已有 `source.md`。

平台细节见 `references/platform-specific.md`。

## Step 1：抓取并生成工作包

| 来源 | 处理方式 |
|---|---|
| 微信公众号 | 可归档为乐享 hyperlink；若要求在线 Markdown 页面则使用文章抓取流程 |
| 免费/付费网页 | `scripts/fetch_article.py fetch "<URL>" --output-dir <DIR>`（默认 CDP） |
| YouTube | `scripts/yt_download_transcribe.py "<URL>" --output-dir <DIR>` |
| 播客 | `scripts/podcast_to_lexiang.py "<URL>" --output-dir <DIR>` |
| PDF / 乐享 PDF | 准备 PDF/解析原文后交给 `trans-doc-to-md` |

三个抓取/转录脚本均以 `source.md` + `meta.json` 为标准输出。YouTube 和播客同时保留
下载媒体、ASR 中间产物；它们不翻译、不上传 Markdown。

## Step 2：内容加工

读取 `meta.json.language`：

- 中文：验证 `source.md` 完整后，由编排流程复制为 `<原文标题>.md`。
- 非中文或语言不确定：调用 `trans-doc-to-md` 的
  **Prepared Markdown Package** 模式，输入整个工作包。该 Skill 负责清洗、双语翻译、
  图片/富元素保真和完整性验证，并输出 `<原文标题>.md`。

不得修改 `source.md`。最终 Markdown 必须继续使用相对图片路径。

## Step 3：乐享目录、去重与上传

目标优先级：用户指定 > 工作区规则 > 本 Skill 的 gitignored `config.json` > 初始化。

1. 获取目标知识库 `root_entry_id`。
2. 查询并复用当天 `YYYY-MM-DD` folder；不存在才创建，使用
   `before=<当前第一条目 ID>` 置顶。
3. 视频/播客在日期目录下查询并复用 `<原文标题>` 文件夹。
4. 在目标目录内按规范化标题、来源 URL 和条目类型去重；确认是同一来源后才覆盖。
5. 调用 uploader：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  "<work-dir>/<原文标题>.md" \
  --parent-id "<目标目录ID>" \
  --name "<原文标题>" \
  --pin \
  --json
```

uploader 版本必须满足 `>=1.1.0,<2.0.0`。它直接渲染
`trans-doc-to-md` 的 callout、表格和图片标注，并完成线上对账。

视频/音频在 Markdown 上传成功后独立归档：

```bash
python3 scripts/upload_video_via_openapi.py "<媒体文件>" \
  --space-id "<SPACE_ID>" \
  --parent-entry-id "<标题目录ID>" \
  --media-type video
```

音频使用 `--media-type audio`。不得用普通文件上传替代 VOD。

## Step 4：交付自检

```text
□ source.md 未被修改，且不是摘要
□ meta.json 标准字段完整，原文标题与来源 URL 可追溯
□ 作者与发布日期来自 canonical meta/time/JSON-LD，并在最终文档顶部只展示一次
□ images/ 中引用文件完整，图文顺序保留
□ 订阅引导、相关推荐、newsletter disclaimer、页脚图片等平台噪音已在抓取转 MD 时过滤
□ 非中文包已通过 trans-doc-to-md 完整性验证
□ 最终文件名为原文标题
□ uploader verified == true，local_images == remote_images
□ 富元素由 uploader 直接渲染，无常规 MCP 二次渲染
□ 文档目录、去重结果和 VOD 媒体目录正确
□ 人工增量修复已同步本地最终 Markdown
□ 浏览器抓取复用了 CDP 上下文；未启动 Google Chrome for Testing
```

## Step 5：自省

用户指出错误、自检失败、发现新平台规律或同类问题再次出现时，更新
`references/lessons-learned.md`。历史根因可保留，但必须明确其旧方案已废弃。

问题归属：

- 抓取、转录、工作包、目录/去重/VOD：本 Skill。
- 清洗、翻译、富元素识别、完整性：`trans-doc-to-md`。
- Markdown 渲染、页面写入和线上对账：`upload-markdown-to-lexiang`。

## 脚本边界

| 脚本 | 职责 |
|---|---|
| `fetch_article.py` | 网页抓取，生成 `source.md`、`images/`、`meta.json` |
| `yt_download_transcribe.py` | YouTube 下载、转录、Show Notes、标准工作包 |
| `podcast_to_lexiang.py` | 播客下载、转录、Show Notes、标准工作包 |
| `lexiang_pdf_parse.py` | 乐享 PDF 来源解析桥接 |
| `upload_video_via_openapi.py` | 视频/音频 VOD 上传 |
| `md_to_pdf.py` | 用户明确要求时生成 PDF |

本 Skill 不包含翻译脚本或 Markdown → 乐享 page 上传脚本。

## 参考文档

- `references/lexiang-upload.md`
- `references/pdf-processing.md`
- `references/youtube-video.md`
- `references/podcast-audio.md`
- `references/platform-specific.md`
- `references/troubleshooting.md`
- `references/lessons-learned.md`
