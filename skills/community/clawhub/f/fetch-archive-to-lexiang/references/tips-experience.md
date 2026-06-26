## 经验总结

### 在线文档图文导入（md_to_page.py）

**核心方案**：Python 脚本通过 HTTP JSON-RPC 直连乐享 MCP API，按图片位置将 markdown 拆分为 text/image 交替段落，逐段导入。

**为什么不走 IDE 的 MCP 工具调用**：
- IDE MCP 工具调用有参数长度限制，45K 字符的 markdown base64 编码后 62K，无法一次性传递
- Python 脚本直连 HTTP JSON-RPC 没有此限制，按 ~15K 字符分段传输即可

**关键踩坑（⚠️ 重要）**：
1. **不要做 base64 编码**：通过 HTTP JSON-RPC 直连时，`entry_import_content_to_entry` 的 content 字段直传原始 markdown 字符串。如果做了 base64 编码，乐享会把 base64 字符串当成纯文本存储，页面显示为乱码。只有通过 IDE MCP 协议调用时才需要 base64
2. **图片需逐张插入**：`block_create_block_descendant` 一次传多张图片的 block 会失败，必须一张一张来
3. **文字分段追加**：第一段用 `force_write=true` 覆盖，后续段用 `force_write=false` 追加到末尾
4. **图片位置要正确**：先按原文中 `![](images/xxx.jpg)` 的位置拆分 markdown，确保文字和图片按原文顺序交替插入
5. **乐享文档名称**：要与文章原标题一致，创建时通过 `--name` 指定，或创建后用 `entry_rename_entry` 修改

**翻译注意事项**：
- **所有英文文章默认必须翻译为中英对照格式再归档**，不可跳过
- 翻译脚本 `translate_gemini.py` 使用 Gemini API（模型：`gemini-2.5-flash`），按 ~4K 字符分段翻译
- Gemini API `gemini-2.0-flash` 已下线，务必使用 `gemini-2.5-flash` 或更新的模型
- 翻译完成后用 `md_to_page.py --entry-id <ID>` 覆盖更新在线文档
- 如果没有 Gemini API Key 也没有 OpenAI API Key，由 AI 助手在对话中翻译后写入文件

**自测清单**（发布前必须完成）：
- [ ] 通过 `entry_describe_ai_parse_content` 验证文字内容可读（非 base64 乱码）
- [ ] 通过 `block_list_block_children` 验证图片 block 存在且有 file_id
- [ ] 验证文档名称与文章标题一致
- [ ] 验证中英对照格式（英文在前，中文翻译紧跟其后）

### YouTube 视频下载与转录

**核心方案**：yt-dlp 下载 → ffmpeg 提取音频 → Whisper 本地转录 → OpenAI API 翻译

**为什么不用 NotebookLM / summarize.sh**：
1. NotebookLM 需要 Google 账号且有额度限制，部分视频可能因版权限制无法提取
2. summarize.sh 依赖外部 API（Apify/YouTube 字幕 API），部分视频无字幕时无法工作
3. Whisper 本地转录**不依赖字幕**，直接从音频波形识别语音，覆盖率 100%

**yt-dlp 版本与安装（关键！）**：
- **必须使用 `brew install yt-dlp`** 安装，不要用 `pip3 install yt-dlp`
- 原因：pip 版本受限于系统 Python 版本（macOS 自带 Python 3.9），无法安装 yt-dlp 的 nightly 版本（需要 Python 3.10+）。而 YouTube 频繁更新反爬策略，旧版 yt-dlp 会遇到 HTTP 403 Forbidden 错误
- brew 安装的 yt-dlp 自带独立 Python 环境，始终能获取最新版本
- 脚本中调用方式：直接用 `yt-dlp` 命令，**不要**用 `python3 -m yt_dlp`

**YouTube DASH 格式 403 错误（重要！）**：
- YouTube 正在强制使用 SABR（Streaming ABR）流媒体协议，传统 DASH 分片下载（`bestvideo+bestaudio`）会触发 HTTP 403 Forbidden
- **解决方案**：优先使用 HLS（m3u8）格式下载，不会被 SABR 拦截
- 脚本中的格式选择顺序：`95-1/94-1/93-1/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best`
  - `95-1`: 720p HLS（推荐，画质和文件大小的最佳平衡）
  - `94-1`: 480p HLS
  - `93-1`: 360p HLS
  - 后面是传统 DASH 格式作为回退
- HLS 格式下载的视频文件会比 DASH 大一些（720p HLS 约 500-600MB vs DASH 约 200-300MB）
- **注意**：`--extractor-args "youtube:player_client=android"` 不支持 cookies，不是可靠的 403 解决方案

**Whisper 转录最佳实践**：
- 音频预处理：16kHz 采样率、单声道 WAV（`ffmpeg -ar 16000 -ac 1`），减少文件大小且是 Whisper 推荐格式
- 段落合并策略：相邻 segment 间隔 <2s 且总时长 <60s 则合并，句号/问号结尾时倾向断开
- 模型选择：默认用 `base`（速度和精度的最佳平衡），重要内容用 `small` 或 `medium`

**翻译策略**：
- 使用 OpenAI `gpt-4o-mini`，分批翻译（每批 10 段），避免 token 超限
- 翻译 prompt 要求"自然流畅的中文表达，专业术语保留英文并附中文注释"
- 中英对照格式：每段先展示英文原文，紧跟中文翻译，段间用空行分隔（不加分隔线和国旗 emoji）
- **如果没有 OPENAI_API_KEY**：脚本会跳过翻译步骤，输出纯英文文字稿。此时可以由 AI 助手在对话中直接翻译全文，然后用 `md_to_page.py --entry-id` 更新乐享文档

**上传乐享的关键决策**：
- 文字稿使用 **在线文档（page）格式**而非文件上传，原因：支持在乐享中按块维度编辑更新，可以逐段修正翻译或补充注释
- 视频使用 **文件（file）格式**上传，因为视频不需要在线编辑
- 上传成功后自动删除本地视频文件，避免占用磁盘空间

**视频上传到乐享的正确方式（重要！）**：
- 通过 lexiang MCP 工具完成，使用三步上传流程：
  1. `file_apply_upload`：申请上传凭证（传入 `parent_entry_id`=日期目录 ID、`upload_type`=PRE_SIGNED_URL、`mime_type`=video/mp4、`size`=文件字节数）
  2. `curl -X PUT` 上传文件到返回的 `upload_url`（预签名 URL，直传 COS）
  3. `file_commit_upload`：确认上传完成（传入 `session_id`）
- 518MB 视频的 PUT 上传约需 30-60 秒

### 播客音频转录

**核心方案**：yt-dlp（generic extractor）下载音频 → ffmpeg 转 WAV → Whisper 转录 → opencc 繁简转换

**yt-dlp 对小宇宙的支持**：
- yt-dlp 没有小宇宙专用 extractor，但 **generic extractor 完全够用**
- 小宇宙页面中嵌入了 `<audio>` 标签，音频直链在 `media.xyzcdn.net`
- 下载不需要 cookies，直接用 `yt-dlp --no-playlist -o "%(title)s.%(ext)s" <URL>` 即可
- 下载速度约 7MB/s，63 分钟播客（59MB）仅需 8 秒

**Whisper 中文转录的繁体问题（重要！）**：
- Whisper base 模型对中文普通话**倾向输出繁体字**（如「歡迎」→ 应为「欢迎」）
- 这是 Whisper 的已知行为，因为训练数据中繁体中文比重较大
- **解决方案**：转录后用 `opencc-python-reimplemented` 的 `t2s`（Traditional to Simplified）模式批量转换
- 安装：`pip3 install opencc-python-reimplemented`
- 用法：`opencc.OpenCC("t2s").convert(text)`

**中文播客 vs 英文 YouTube 的流程差异**：
- 中文播客**不需要翻译**，但**需要繁简转换**
- 播客音频是直接的 m4a/mp3 文件，**不需要从视频中提取音频**（但仍需 ffmpeg 转为 WAV 格式给 Whisper）
- Whisper 转录时**指定 `language='zh'`** 可以提高中文识别准确率
- 上传乐享时 MIME 类型用 `audio/mp4`（m4a）或 `audio/mpeg`（mp3），不是 `video/mp4`

**转录性能参考**：
- 63 分钟中文播客 → Whisper base 模型在 CPU 上转录耗时约 115 秒
- 产出 2496 个 segments，合并后 65 个段落

### 微信公众号图文抓取

**核心问题**：`web_fetch` 工具无法获取微信公众号文章的图片（懒加载 + 防盗链），**必须**使用 `fetch_article.py`。

**技术原理**：
1. **懒加载机制**：微信图片的真实 URL 存放在 `data-src` 而非 `src`，依赖 `IntersectionObserver` 在元素进入视口时才加载。Playwright 无头浏览器通过 `window.scrollBy(0, 300)` 配合 `asyncio.sleep(0.2)` 模拟慢速滚动，逐步触发所有图片的懒加载观察器
2. **兜底策略**：滚动完成后，通过 `page.evaluate()` 遍历所有 `img[data-src]`，将未被触发的 `data-src` 强制复制到 `src`
3. **高清图优先**：提取图片 URL 时优先使用 `data-src`（高清原图），而非 `src`（可能是低分辨率占位图）
4. **格式识别**：微信图片 URL 无常规扩展名（如 `mmbiz.qpic.cn/...?wx_fmt=png`），需解析 `wx_fmt` 查询参数推断文件格式
5. **防盗链绕过**：通过 Playwright 页面上下文的 `page.request.get()` 下载图片，自动携带正确的 Referer 头
6. **专用选择器**：微信文章有固定 DOM 结构（`#js_content`、`#activity-name`、`#js_name`、`#publish_time`），使用专用选择器比通用选择器更精准可靠

**关键决策**：
- 微信文章是公开可读的，跳过登录检测和 Cookie 注入流程
- 滚动参数（300px 步长、200ms 间隔）经实测可平衡速度与懒加载触发成功率
- Markdown 转换时 `imageMap` 同时匹配 `src` 和 `data-src`，确保无论 HTML 中引用哪个属性都能正确替换

**验证标准**：抓取完成后检查 `article_meta.json` 中的 `image_count` 字段，与原文图片数量比对，确认无遗漏。

### LEXIANG_TOKEN 过期时的图文上传降级方案

**场景**：`md_to_page.py` 依赖 `LEXIANG_TOKEN`，token 有效期约2小时，过期后图片上传全部失败（401）。

**降级方案（MCP connector "先全文后补图"）**：
1. `entry_import_content` / `entry_import_content_to_entry` 一次性导入全文（MCP connector 不受 token 过期影响）
2. `block_list_block_children` 获取页面所有 block 列表
3. 通过文本锚点找到每张图片应插入的位置（block index）
4. 逐张上传：`block_apply_block_attachment_upload`（MCP）→ `curl -X PUT`（presigned URL）→ `block_create_block_descendant`（MCP，指定 insert index）
5. **每插入一张图片后，后续图片的 insert_index 需 +1**

**锚点匹配技巧**：
- 英文原文和中文翻译中的关键短语可作为锚点
- 用 `get_block_text()` 提取每个 block 的文本内容进行匹配
- 对于跨语言锚点，用中文翻译文本搜索更可靠

### 🚨 entry_import_content 图片语法禁区（2026-06-03 实战验证）

**核心结论**：`entry_import_content` 和 `entry_import_content_to_entry` 的 content 参数中，**任何图片语法都会产生空图片 block**，包括：
- ❌ `![alt](https://cdn.example.com/img.png)` — Markdown 图片语法 → 空 image block
- ❌ `<image src="https://cdn.example.com/img.png"/>` — XML block 语法 → 空 image block
- ❌ `![alt](images/local.png)` — 本地路径引用 → 空 image block

**空图片 block 的特征**：`block_type: "image"`, 有 `width` 属性，但**无 `file_id`**，页面显示为空白占位符。

**正确做法**：图片只能通过 block 级 API 三步流程上传：
1. `block_apply_block_attachment_upload(entry_id, name, size, mime_type)` → 获取 `session_id` + `upload_url`
2. `curl -X PUT "<upload_url>" -H "Content-Type: image/png" --data-binary @<图片路径>` → 上传到 COS
3. `block_create_block_descendant(entry_id, parent_block_id, index, descendant=[{block_type: "image", image: {session_id}}])` → 创建图片 block

**关键参数注意事项**：
- `block_apply_block_attachment_upload` 的 `size` 参数**必须是字符串**（如 `"54541"`），传整数会参数校验失败
- `curl PUT` **必须带 `Content-Type` header**（如 `-H "Content-Type: image/png"`），否则 COS 返回 `SignatureDoesNotMatch`
- `block_update_block` **不支持更新 image block 的 session_id/file_id**，无法把空图片 block 修复为正常图片 block
- 修复空图片 block 的唯一方法：`block_delete_block` 删除 → `block_create_block_descendant` 重新创建

**多图片插入的 index 计算策略**：
- **从后往前插入**：先插入 index 最大的图片，避免前面插入导致后续 index 偏移
- 如果从前往后插入：每插入一张图片，后续图片的 index 需 +1

### markdownify 图片引用丢失问题

**问题**：使用 `markdownify` 时传 `strip=["img"]` 参数会完全移除图片标签，导致 Markdown 中无 `![](images/xxx)` 引用。

**修复**：不要传 `strip` 参数，或在转换后从原始 HTML 中重新提取图片位置信息并插入到 Markdown 中。

### COS 图片上传 403 问题

**问题**：通过 `curl -X PUT` 上传图片到 COS presigned URL 时返回 403 Forbidden。

**原因**：presigned URL 签名中包含了 `content-length` 和 `content-type` 的 signed headers，如果请求中缺少这两个 header 或值不匹配，COS 会拒绝请求。

**修复**：上传时必须带上 `Content-Type` 和 `Content-Length` 两个 header：
```bash
FILE_SIZE=$(stat -f%z "images/img_01.png")
curl -X PUT "<upload_url>" \
  -H "Content-Type: image/png" \
  -H "Content-Length: $FILE_SIZE" \
  --data-binary @"images/img_01.png"
```
- `.png` → `image/png`，`.jpg`/`.jpeg` → `image/jpeg`

### 翻译时图片引用丢失问题

**问题**：对英文文章翻译为中英对照格式时，图片引用 `![](images/xxx)` 未被保留到翻译版 Markdown 中。

**原因**：翻译是基于纯文字版（无图片引用）进行的，翻译后缺少图片位置信息。

**修复方案**：
1. 基于带图片引用的原文 Markdown 进行翻译，翻译时保留 `![](images/xxx)` 引用不动
2. 如果已翻译完毕但缺少图片引用，可通过锚点匹配将图片引用插入翻译版：
   - 提取英文原文中每张图片前后的关键短语作为锚点
   - 在翻译版 Markdown 中搜索对应的中文翻译锚点
   - 在匹配位置插入图片引用
3. 部分锚点因引号/标点编码差异可能无法自动匹配，需手动修复

### block_list_block_children _mcp_fields 格式

**问题**：`_mcp_fields` 参数传 JSON array 格式（如 `["-blocks.text"]`）导致参数验证失败。

**修复**：`_mcp_fields` 使用逗号分隔字符串格式，如 `"-blocks.text,-blocks.heading1,-blocks.heading2"`。

### 新平台适配思路

适配新平台时，需依次识别和处理以下 4 个维度：
1. **懒加载机制** — 图片是否用 `data-src`、`data-lazy` 等延迟加载？需要怎样的滚动策略触发？
2. **专用 DOM 结构** — 正文、标题、作者、日期的选择器是什么？
3. **图片 URL 格式** — 扩展名是否在路径中？是否需要从查询参数推断？
4. **防盗链策略** — 是否需要正确的 Referer？是否有其他鉴权机制？

