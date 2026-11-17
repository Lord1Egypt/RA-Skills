# 元信息输入与输出约定

输入是 UTF-8 JSON：顶层只有 `assets`，为非空数组。Agent 完成文字撰写后再调用工具；脚本不从说明生成文章、alt、图注或字幕。未知字段会被拒绝，避免拼错字段后静默丢失资料。完整可运行输入见[截图与视频](../examples/success/input.json)及[音频](../examples/success/audio-input.json)。

## 各媒体共有字段

| 字段 | 类型与处理 |
| --- | --- |
| `id` | 必填，批内唯一的非空字符串；用于交接对照 |
| `type` | 必填，`image`、`video` 或 `audio` |
| `original_filename` | 必填，仅文件名，不含目录；原始扩展名会原样保留 |
| `evidence` | 必填对象，见下节 |
| `filename_stem` | 可选，不含扩展名的建议名称；缺省使用原文件名的主干 |
| `title` | 可选，已知标题；未知留空。不能从未见画面推断标题 |
| `caption` | 可选，由 Agent 依据内容撰写的图注或简短说明；缺省 `null` |
| `content_url` | 可选，用户已提供的媒体 HTTP(S) 地址，不是本机路径 |
| `page_url` | 可选，媒体所在正文的 HTTP(S) 地址，进入 JSON-LD 的 `isPartOf` |

地址仅做格式检查，不联网验证可达性、公开性或归属，不接受内嵌用户名/密码。路径式附件引用只用于下述 `subtitles/transcript.reference`，不会被脚本打开。

`filename_stem` 保留 Unicode 字母、数字、组合标记、连字符和下划线，空格、点、斜线和其他符号转为连字符；不改原文件。文件名主干限120个 UTF-8 字节，批内按 Unicode NFC 和不区分大小写判断重名，并加 `-2`、`-3` 等后缀。Windows 保留名如 `CON` 加 `asset-` 前缀。全符号名称报错，不生成空名称。同批以外的目标目录冲突需交付方另核对。

支持的扩展名（不区分大小写校验，建议名保留原大小写）：

- image：`.png .jpg .jpeg .webp .gif .svg .avif .heic .heif .tif .tiff .bmp .ico`
- video：`.mp4 .mov .m4v .webm .mkv .avi .mpeg .mpg .3gp .m2ts .ts .ogv`
- audio：`.mp3 .wav .flac .m4a .aac .ogg .oga .opus .aiff .aif .wma .m4b`

不支持的扩展名、缺扩展名或类型冲突会报错。脚本不检查二进制格式；扩展名可接受不表示 Agent 能读取该媒体。类型冲突应确认原文件，不通过把后缀改成 `.jpg` 消除错误。

## 内容依据 evidence

```json
{
  "kind": "user_description",
  "scope": "excerpt",
  "reference": "用户提供的00:00–00:10片段说明",
  "details": "开头介绍项目操作流程。"
}
```

- `kind`：`reviewed` 表示 Agent 实际查看或听取；`user_description` 表示仅依用户说明；`unavailable` 表示无内容依据。
- `scope`：`full` 为覆盖整个素材的查看或说明；`excerpt` 为片段，在 `reference` 标明页区或时间范围；无依据必须为 `none`。
- `reference`：必填，非空来源说明，可用附件名、消息编号和时间段。不要填写私有机器的绝对路径或凭据。
- `details`：已有依据时必填，记录客观内容；无依据时不填或为 `null`。

`unavailable` 条目不接受非空 alt、caption 或 description。此时保留已知标题、命名、时长等独立事实，内容文字为 `null`。脚本无法判断人类撰写的描述是否真实，最终内容复核由 Agent 完成，不能把 `user_description` 改成 `reviewed` 来表示脚本运行成功。

## image 专用字段

| 字段 | 规则 |
| --- | --- |
| `decorative` | 布尔值，默认 false；由图片在页面中的作用决定 |
| `alt` | 信息图片为有依据的非空文字；未能完成标注时为 null 或省略；纯装饰图必须为空或省略，输出统一为 `""` |

图片不接收视频时长、音频文字稿等字段。装饰图无 JSON-LD，`schema.status` 为 `not_applicable`。装饰图仍保留依据状态，避免把空 alt 当作实际已查看。

## video / audio 字段

| 字段 | 规则 |
| --- | --- |
| `description` | 有内容依据的简介；不是脚本根据标题生成的文字 |
| `duration_seconds` | 实际已知秒数，有限且大于0，可含小数；缺省或 null 为待补，不接受字符串、布尔值、0、负数或非有限数 |
| `upload_date` | 已知真实上传日，`YYYY-MM-DD`；或有时区的 ISO 时间，例如 `2026-10-18T10:00:00+08:00`。不以制作日期、今天或文件修改时间代填 |
| `chapters` | 可选数组，条目只有 `start_seconds` 和非空 `title`；起点非负、严格递增，已知时长时必须小于时长；未知起点不能填0占位 |

视频另接受 `thumbnail_url` 和 `subtitles`；音频另接受 `transcript`。两者均不接收 `alt/decorative`；音频不接收 `thumbnail_url/subtitles`。视频章节未提供或为空时进入待补清单；音频章节可选，不将省略自动视为缺陷。

`subtitles/transcript` 对象：

```json
{"status": "provided", "reference": "用户附件：片段字幕.vtt"}
```

- `provided` 必须有非空 `reference`；只表示用户给出了引用，不表示脚本已读取或验证文件。
- `missing` 不带引用，可附 `reason`；字段省略时也按 missing 处理。
- `not_applicable` 不带引用，必须有 `reason`，如“纯提示音，无语言内容”。

上传日期、时长、章节、封面及附件均视为调用方提供的事实，脚本不探测媒体；Agent 需在交接前核对来源。缺字幕时只列需求，不自动造字幕；本工具不解析 SRT/VTT。

## 输出与状态

两份交付文件使用相同逐项结果。JSON 顶层有 `schema_version`、说明、`summary` 和 `assets`；summary 按实际输入数量统计类型、依据类别和待补条目，不含 AI 引用或搜索表现指标。

逐项保留原文件名、建议名、依据、用户提供或 Agent 撰写的文字、类型专属元信息、`gaps` 和 JSON-LD。`null` 为未知，不能当作0、空字幕或已验证。`duration_iso8601` 是确定性换算，例如125秒→`PT2M5S`。

`gaps` 列出缺失字段：共有的标题、公开地址、图注；信息图片的 alt；视频/音频的简介、时长和上传日期；视频的封面、字幕和章节；音频的文字稿。装饰图不要求这些发布资料。缺内容依据时单列 `evidence`。

- `status: needs_information`：仍有待补项；`ready_for_review`：本工具列出的资料齐全，仍需 Agent 复核。
- `schema.status: partial`：JSON-LD 交接字段不齐；`fields_present`：齐全，但未经搜索引擎验证；`not_applicable`：装饰图。
- 图片 JSON-LD 交接字段为 `name/description/contentUrl`，description 取已有 caption，其次取 alt。视频另检查 `uploadDate/duration/thumbnailUrl`；音频另检查 `uploadDate/duration`。这些是本工具的交接范围，不声称等于某平台全部必需属性。
- 仅给定字段进入 JSON-LD，不把 null、猜测日期、占位URL、虚构作者或分数写入；给定章节转为 `hasPart` 中的 `Clip`，保留名称与 `startOffset`。

命令从技能根目录运行：

```sh
python3 scripts/build_metadata.py --input examples/success/input.json --output-dir output
```

退出0表示输入合法、两份交付已写入，可以仍有待补项；退出2表示输入或文件操作失败。数据校验先于文件写入，输入非法时不覆盖原有交付；文件系统写入失败仍需检查输出目录是否只有部分文件。只实现 `--input`、`--output-dir` 及 argparse 的 `--help`，不提供关键词、改名、上传或转码参数。
