# fetch-archive-to-lexiang

将网页、YouTube、播客和 PDF 来源整理为统一工作包，并编排目录去重、Markdown 页面上传
和视频/音频 VOD 归档。

## v4 架构

```text
来源侦察与抓取                  内容加工                         页面写入
fetch-archive-to-lexiang  →  trans-doc-to-md  →  upload-markdown-to-lexiang
工作包/目录/去重/VOD           清洗/翻译/完整性/富元素             渲染/上传/线上对账
```

依赖版本：

- `trans-doc-to-md >=3.0.0,<4.0.0`
- `upload-markdown-to-lexiang >=1.1.0,<2.0.0`

本 Skill 不包含翻译实现，也不包含 Markdown 页面上传实现。

## 标准工作包

```text
<work-dir>/
├── source.md
├── images/                 # 可选
├── meta.json
└── <原文标题>.md           # 内容加工后的最终文件
```

`source.md` 是不可变原文。`meta.json` 至少包含：

```json
{
  "title": "归档标题",
  "source_url": "https://...",
  "source_title": "原文标题",
  "source_type": "article|youtube|podcast|pdf",
  "language": "zh|en|...",
  "parent_id": "可选"
}
```

中文内容由编排流程复制为标题文件；非中文内容将整个 Prepared Markdown Package 交给
`trans-doc-to-md`，由其生成最终标题 Markdown。

## 支持来源

| 来源 | 本 Skill 产物 |
|---|---|
| 网页/付费文章 | `source.md`、`images/`、`meta.json` |
| YouTube | 视频、转录 `source.md`、`meta.json` |
| 播客 | 音频、Show Notes、转录 `source.md`、`meta.json` |
| PDF / 乐享 PDF | PDF/解析桥接产物，随后交给 `trans-doc-to-md` |

## 脚本

```text
scripts/
├── fetch_article.py
├── yt_download_transcribe.py
├── podcast_to_lexiang.py
├── lexiang_pdf_parse.py
├── upload_video_via_openapi.py
└── md_to_pdf.py
```

### 抓取文章

```bash
python3 scripts/fetch_article.py fetch "<URL>" --output-dir <工作目录>
python3 scripts/fetch_article.py fetch "<URL>" --output-dir <工作目录> --cdp
```

### YouTube

```bash
python3 scripts/yt_download_transcribe.py "<YouTube URL>" \
  --output-dir <工作目录> \
  --whisper-model base
```

`--skip-translate` 仅为旧调用兼容保留，会打印 deprecated 警告；脚本始终不翻译。

### 播客

```bash
python3 scripts/podcast_to_lexiang.py "<播客 URL>" \
  --output-dir <工作目录> \
  --language zh \
  --metadata-json metadata.json \
  --chapters-json chapters.json \
  --hotwords-json hotwords.json
```

播客脚本只生成工作包和音频产物，不接受乐享上传参数。

## 乐享归档

本 Skill 负责查找/创建日期目录和视频/播客标题目录，并在上传前按标题、来源 URL 与类型
去重。所有 Markdown 页面写入调用 uploader：

```bash
python3 "<uploader-root>/scripts/lexiang_upload.py" upload \
  "<工作目录>/<原文标题>.md" \
  --parent-id "<目标目录ID>" \
  --name "<原文标题>" \
  --pin \
  --json
```

正常富元素由 uploader 直接渲染 `trans-doc-to-md` 标注。只有上传后少量人工修复
可使用 block 工具，并且必须同步本地最终 Markdown。

视频/音频使用独立 VOD 脚本：

```bash
python3 scripts/upload_video_via_openapi.py "<媒体文件>" \
  --space-id "<SPACE_ID>" \
  --parent-entry-id "<标题目录ID>" \
  --media-type video
```

音频改为 `--media-type audio`。

## 配置

复制 `config.json.example` 为 gitignored `config.json`，或在任务中明确指定知识库。
个人上传凭证由 `upload-markdown-to-lexiang` 管理；VOD 使用
`~/.lexiang/openapi.json`。

## 设计约束

- 不得覆盖内容不同的既有 `source.md`。
- 不得用摘要替代原文，不得删除图片引用。
- 不得在本 Skill 或当前 Agent 中实现翻译。
- 不得恢复旧 Markdown 导入或文件上传路径。
- 视频/音频必须走 VOD 路径，普通文件上传不会触发转码。

## License

MIT
