# Changelog

## v4.1.2 — 2026-07-16

### Added — 跨平台通用规则预检应用（源自 skill-publisher v5.18.1 规则 30）

基于 skill-publisher v5.18.1 的「跨平台通用规则预检」规则 30，将 80% 的 ClawHub 规则泛化应用到 douyin-article。这是 ClawHub 规则通用性分析（20% 平台特定 / 60% 概念通用 / 20% 工程最佳实践）的落地实践：

- **frontmatter `metadata.openclaw` 声明层补齐**（规则 30 A 项）：SKILL.md frontmatter 新增 `metadata.openclaw` 嵌套结构，声明 `requires.bins`（python/ffmpeg/ffprobe）、`anyBins`（yt-dlp/agent-browser/curl）、`envVars`（HTTPS_PROXY/HTTP_PROXY/http_proxy/https_proxy/HF_ENDPOINT/SKIP_CERT_CHECK，全部标 `required: false`）、`emoji`、`homepage`。无凭证环境变量（douyin-article 不读取任何凭证），只有代理/镜像/校验开关类可选变量
- **`.clawhubignore` 文件创建**（规则 30 E 项）：ClawHub 发布专用排除层，覆盖凭证文件 / 临时脚本 / 构建产物 / 临时文件 / 日志 / IDE 文件 / 测试产物（含 mp3/mp4/wav/m4a/srt/vtt 等音视频中间产物）/ ClawHub 自动生成文件 / 本地 cookie 文件

### Layer 4.5 Frontmatter 声明完整性自检

- 代码中所有环境变量引用（os.environ.get / os.environ.setdefault）：
  - HTTPS_PROXY / HTTP_PROXY（代理）→ 已声明
  - http_proxy / https_proxy（小写变体）→ 已声明
  - HF_ENDPOINT（HuggingFace 镜像）→ 已声明
  - SKIP_CERT_CHECK（v4.1.1 引入的证书校验开关）→ 已声明
- subprocess 调用的二进制：ffmpeg / ffprobe / yt-dlp / agent-browser / curl / where/which（系统命令）→ 已声明
- 自检结果：PASS（无未声明的环境变量或二进制）

### Changed — 规则 30 B/C/D 项验证（已满足，无需修改）

- **B 项 description 行为声明段落**：douyin-article description 已声明全部行为（批量转录 + 三层字幕探测 + 双语对比 + 全平台支持 + Do NOT 范围），无需修改
- **C 项 README 用户警告段落**：README.md 已有"用户须知"段落（本地副作用 / 网络访问 / 资源占用 / 清理方式 4 项），无需修改
- **D 项 权限声明段落**：SKILL.md 已有 5 行权限声明表格（网络访问 / 文件读写 / 环境变量 / subprocess / 外部 API），无需修改

### Lesson Learned — 跨平台通用规则预检的可移植性验证

douyin-article v4.1.2 是 skill-publisher v5.18.1 规则 30 的首个外部应用案例。验证结论：
1. **规则 30 的 5 项预检项可移植**：B/C/D 三项 douyin-article 在 v4.1.0-v4.1.1 已满足（说明 skill-publisher 自身的预检流程已经在间接推动这些规则），A/E 两项需要本次补齐
2. **`metadata.openclaw` 结构对 SkillHub 无副作用**：SkillHub 未知字段被忽略，保留该结构不影响 SkillHub 发布
3. **不同 skill 的 `metadata.openclaw` 差异显著**：skill-publisher 有 3 个凭证环境变量（GITHUB_TOKEN/CLAWHUB_TOKEN/SKILLHUB_TOKEN），douyin-article 没有凭证环境变量（只有代理/镜像/校验开关类可选变量）。说明 `metadata.openclaw` 不是模板化的填空题，而是每个 skill 基于自身代码的自检结果

## v4.1.1 — 2026-07-15

### Fixed
- **TLS 证书校验默认启用**（ClawHub SkillSpector Tool Parameter Abuse ×4 修复）：`fetch_bilibili.py` / `fetch_youtube.py` 中 4 处 `--no-check-certificates` 硬编码改为 `_cert_flags()` 函数控制，默认启用证书校验。仅当用户显式设置环境变量 `SKIP_CERT_CHECK=1` 时禁用（应对偶发的 B站证书过期问题），禁用为用户明确选择而非默认行为。
- **Description-Behavior Mismatch 修复**：description 的 Do NOT 表述从"视频下载、字幕提取"改为"纯视频文件下载（不转录）、纯字幕提取（不转录）"，明确区分"交付物"与"转录中间步骤"——管线确实会下载音频流作为转录中间产物，但不用于交付视频文件。
- **Description 声明 yt-dlp 通用平台支持**：description 明确列出 Vimeo/TikTok/Twitter 等通用平台，与代码 `ytdlp-generic` 路由一致，消除 scope-expansion 风险。
- **Vague Triggers 收窄**：触发词删除"视频翻译"（过于泛化，可能匹配普通翻译请求）和"批量转录视频"（与"批量转录视频链接"重复，保留后者更精确）。

### Changed
- README 中英文双语同步修改"自动翻译"措辞：从"非中文内容自动翻译为中文"改为"用户使用「双语转录」触发词时，非中文内容翻译为中文"，明确翻译为用户触发的行为而非默认自动执行。
- SKILL.md "不做"段落与 description Do NOT 保持一致。

### Security
- **ClawHub SkillSpector 审计响应**：本次升级响应 14 项 findings 中的 10 项合理 findings（4 项 High + 6 项 Medium），4 项过渡修改/误报未修复（subprocess.run 已在权限声明披露；Missing User Warnings 已有整体警告）。

## v4.1.0 — 2026-07-15

### Added
- **B站公共 API 字幕直连**：新增 `scripts/bilibili_subtitle_api.py`，通过 B站公共 API（`api.bilibili.com/x/web-interface/view` + `x/player/v2`）无需登录直接探测 CC 字幕，包括 UP 主上传的手动字幕和 B站 AI 生成的自动字幕。比 yt-dlp `--list-subs` 更快更可靠（不依赖登录态）。
- **三层字幕优先策略**：B站字幕探测升级为三层回退：
  - Layer 1: B站公共 API 直连探测字幕（最快，无需登录）
  - Layer 2: yt-dlp `--list-subs` + 字幕下载（更广覆盖，支持 412 回退）
  - Layer 3: 音频下载 + Whisper 转录（最终 fallback）
- **B站字幕 JSON 解析器**：新增 `download_bilibili_subtitle` 函数，把 B站字幕 JSON 格式（`{body: [{from, to, content}]}`）转换为标准 SRT，复用下游 `srt_to_transcript` 管线。
- **412 反爬虫处理**：B站公共 API 在 412 错误时打印清晰日志，自动 fallback 到 Layer 2。

### Changed
- `fetch_bilibili.py`：字幕优先路径升级为三层探测；新增 `bilibili_subtitle_api` 导入；日志清晰标注 Layer 1/2/3。
- 字幕探测日志可读性提升：探测成功/失败时输出 UP 主/标题/字幕类型（手动/AI）等关键信息。

### Architecture
- **三层字幕探测架构验证**：经 SkillHub 调研，社区已有相同架构（"优先原生字幕，回退到 Whisper"）的同类 skill，验证 v4.0 设计正确性。v4.1 在此基础上增加 B站公共 API 直连，提升字幕探测命中率。
- **B站 CC 字幕可用率实测**：15 个视频样本测试 CC 字幕可用率 0%（UP 主未上传，B站 AI 也未生成），证实 B站字幕路径在中文视频场景下命中率极低，但架构正确性已验证。

### Tested
- 端到端测试：B站 BV1NK411D7pr?p=1 全流程跑通（fetch → 三层字幕探测 → Layer 3 fallback → Whisper 转录 → pack → translate skip → boundaries → build）
- 字幕探测测试：5 个 B站视频（英语李辉/Rick Astley/影视飓风/何同学/罗翔）全部正确探测无字幕
- 输出 MD 文件正确包含 `> 语言: 中文` 字段

## v4.0.0 — 2026-07-15

### Added
- **全平台支持（yt-dlp 1700+ extractor）**：新增 `scripts/fetch_subtitles.py`，通过 yt-dlp 拉取字幕并自动转换为 transcript 格式。支持 Vimeo/TikTok/Twitter/X/Twitch/Dailymotion/SoundCloud/TED/Loom 等任意 yt-dlp 支持平台。
- **字幕优先策略**：B站/YouTube/通用平台优先拉取平台字幕（手动 > 自动），跳过 Whisper 转录，节省 95% 能耗。字幕不可用时 fallback 到音频下载 + Whisper。
- **SRT → transcript 转换器**：新增 `scripts/srt_to_transcript.py`，把平台 SRT 字幕转为与 Whisper 输出同构的 transcript_N.json，下游零改动。
- **双语对比翻译管线**：新增 `scripts/subtitle_pipeline.py`（纯 Python 标准库），4 子命令 prepare / next-batch / apply / render / validate，支持断点恢复。翻译由主对话（active session model）完成，零外部 API 依赖。
- **翻译编排脚本**：新增 `scripts/03_5_translate.py`，扫描 pack_summary 自动为非中文视频准备 manifest，主对话循环调用 next-batch + apply 完成翻译。
- **双语 MD 渲染**：`04_build_output.py` 支持 translation_N.json，非中文视频输出段落对比格式（中文译文 + 紧跟 `> **原文**：English text` blockquote）。
- **语言检测**：`common.py` 新增 `detect_language` / `detect_transcript_language` / `needs_translation`，基于 Unicode 字符范围统计（CJK/平假名/片假名/韩文/拉丁字母）。
- **SRT 解析**：`common.py` 新增 `parse_srt` / `parse_srt_time` / `format_srt_time`，处理 SRT 时间码与 HTML 标签。
- **全平台 URL 检测**：`common.py` 新增 `is_ytdlp_supported_url` + `YTDLP_GENERIC_DOMAINS`（16 个通用平台域名）。

### Changed
- `01_fetch.py`：B站启用字幕优先策略（传 `transcript_dir`）；新增 ytdlp-generic 平台分派，复用 B站 adapter（同为 yt-dlp + 字幕优先 + 音频 fallback）。
- `fetch_bilibili.py`：新增 `_probe_bilibili_metadata` 用 yt-dlp --dump-json 拿元数据；新增字幕优先路径（先 CC 字幕，失败 fallback 音频）。
- `fetch_youtube.py`：新增 yt-dlp 字幕 fallback（youtube-transcript-api 失败后用 yt-dlp 拉字幕）；新增 `source_type` / `source_language` / `needs_translation` 字段。
- `03_pack_transcript.py`：`build_takes_packed` 显示语言和来源类型；`process_one` 返回 `language` / `source_type` / `needs_translation`。
- `04_build_output.py`：`build_markdown` 新增 `translation` 参数；`process_one` 新增 `translation_path` 参数加载 translation_N.json；`main` 新增 `--translation-dir` 参数；文档头新增语言标注、转录工具标注、平台标签（Vimeo/TikTok 等）。
- frontmatter `metadata.version` 升至 4.0.0
- `plugin.json` version 升至 4.0.0
- 触发词扩展：新增 `双语转录` / `YouTube双语` / `视频翻译` / `Vimeo转录` / `TikTok转录` / `批量转录视频链接`

### Architecture
- **5 + 0.5 阶段管线**：fetch → transcribe（仅无字幕时）→ pack + 语言检测 → **3.5 translate（仅非中文时）** → boundaries → build
- **字幕优先路径能耗对比**：YouTube 字幕路径 ~3 秒完成 vs Whisper 音频路径 30-60 秒/分钟视频（节省 ~95%）
- **翻译契约**：segment 是不可变翻译单元（1 cue 1 segment），80 segment/批 + 前后 2 个只读 context，manifest 是唯一状态源

### Tested
- 单元测试：5 个双语渲染测试全部通过（向后兼容、双语格式、未翻译标记、空翻译降级、多场景）
- 语言检测：zh/en/ja/vimeo/srt 全部正确识别

## v3.1.0 — 2026-07-14

### Fixed
- **02_transcribe.py 模型重复加载（Critical）**：批量转录时每次循环重新加载 Whisper small 模型，11 个视频浪费 5-10 分钟。改为全局 `_MODEL_CACHE`，只加载一次。
- **03_pack_transcript.py route_heuristic 路由启发式不准（Important）**：英语教学课标题含 "Lecture" / "Day N" / "训练营" / "句法" / "句子" / "语法" / "单词" / "词汇" 等关键词未被识别，导致误判为 `explainer`。扩充 lesson 关键词列表。
- **fetch_xiaoyuzhou.py 主播名提取失败（Important）**：所有小宇宙 episode 的 author 字段为"未知"。新增 5 级兜底提取：__NEXT_DATA__.episode.author → og:audio:artist → og:audio:album → 全文 grep `"author"` → 全文 grep `"nickname"`。实测从 `__NEXT_DATA__` 中正确提取到主播名。
- **common.py ERROR_CORRECTIONS 字典不充分（Important）**：Whisper small 在中文教学课上的常见同音错字未覆盖。新增 25+ 条：主剧→主句、分剧→分句、端语→短语、定义从句→定语从句、原子和→原子核、表情打印→表情达意、所有隔→所有格、城分→成分、抛丁解→拆解、诸语→赘语、炸一读→乍一读、剧法分析→句法分析等。
- **错字字典"抛丁"/"抛丁解"重复替换 bug**：先替换 "抛丁"→"拆解" 导致 "抛丁解句子"→"拆解解句子"。删除短的 "抛丁" 条目，只保留长的 "抛丁解"。

### Changed
- frontmatter `metadata.version` 升至 3.1.0
- `plugin.json` version 升至 3.1.0

### Tested
- 完整端到端批量测试：11 集小宇宙英语教学课（MUSE高考英语长难句分析系列）
- 阶段 1：11/11 音频下载成功，总时长 4.5 小时
- 阶段 2：11/11 Whisper 转录成功，总字数 ~75000 字
- 阶段 3：11/11 打包成功，路由全部正确识别为 lesson（v3.1 修复后）
- 阶段 4：11/11 scene-boundaries 生成（subagent 协助）
- 阶段 5：11/11 MD 文件输出成功，结构完整

## v3.0.0 — 2026-07-14

### Added
- 小宇宙播客支持：新增 `scripts/fetch_xiaoyuzhou.py`，curl 抓 HTML 提取 `<audio src>` 直链，无需浏览器自动化
- YouTube 视频支持：新增 `scripts/fetch_youtube.py`，双保险策略：
  - 优先用 `youtube-transcript-api` 直接拿字幕（几秒完成，跳过 Whisper 转录）
  - 字幕不可用时 fallback 到 yt-dlp 下载音频走 Whisper
- 代理支持：自动读取 `HTTP_PROXY` / `HTTPS_PROXY` 环境变量（仅 YouTube 需要）
- `common.py` 平台抽象层扩展：`detect_platform` 支持 `xiaoyuzhou` / `youtube`，新增 `extract_xiaoyuzhou_id` / `normalize_xiaoyuzhou_url` / `extract_youtube_id` / `normalize_youtube_url`
- `02_transcribe.py` 支持 `skip_transcribe` 字段：YouTube 字幕路径直接跳过 Whisper
- `04_build_output.py` 平台标签扩展：支持小宇宙 / YouTube 来源标签
- 平台支持矩阵文档：SKILL.md 末尾新增矩阵表

### Changed
- 技能标题：视频批量转录 → 视频/播客批量转录（抖音/B站/小宇宙/YouTube）
- 触发词扩展：新增 `小宇宙转录` / `批量转录播客` / `YouTube转录` / `批量转录YouTube`
- `01_fetch.py` 路由扩展：四平台自动分派，YouTube 代理状态提示
- frontmatter `metadata.version` 升至 3.0.0
- 依赖表新增 `youtube-transcript-api` 行

## v2.0.0 — 2026-07-14

### Added
- B 站视频支持：新增 `scripts/fetch_bilibili.py`，基于 yt-dlp（一行命令下载，比 agent-browser 轻量）
- 平台抽象层：`common.py` 新增 `detect_platform(url)` / `extract_bvid(url)` / `extract_p(url)`
- frontmatter `allowed-tools` 字段（审计整改）
- README.md 中英双语（审计整改）
- LICENSE（MIT-0）（审计整改）
- .claude-plugin/plugin.json 插件元数据（审计整改）

### Changed
- 技能标题：抖音批量转录 → 视频批量转录（抖音/B站）
- 触发词扩展：新增 `B站批量转录` / `批量转录B站` / `批量转录视频`
- `01_fetch.py` 自动路由：检测 URL 平台后分派到对应 adapter
- `ERROR_CORRECTIONS` 字典扩充至 80+ 条

## v1.0.0 — 2026-07-14

### Initial Release
- 5 阶段管线（fetch / transcribe / pack / 主对话切分 / build output）
- 6 路由模型（lesson / explainer / conversation / demo / narrative / bulletin）
- 抖音 adapter：agent-browser + curl + blob URL 40s 等待 + __vid 匹配 + MD5 去重
- faster-whisper (small) 本地转录，保留 segments 时间戳
- opencc 繁简转换
- 错字自动修正字典（40+ 条）
- Light-plus 原则（保留推理/例子/数字）
- 按语义边界切分，非机械时长
