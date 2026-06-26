## 常见问题

| 问题 | 原因 | 修复方法 |
|------|------|----------|
| YouTube 视频下载 HTTP 403 Forbidden | yt-dlp 版本过旧 + YouTube 强制 SABR 流媒体协议，传统 DASH 分片下载被拦截 | ① `brew install yt-dlp` 升级到最新版（不要用 pip）；② 脚本已配置优先使用 HLS(m3u8) 格式（`95-1/94-1/93-1`），自动回退 |
| `pip3 install --upgrade yt-dlp` 无法安装最新版 | macOS 自带 Python 3.9，yt-dlp nightly 版需要 Python 3.10+ | 改用 `brew install yt-dlp`，brew 版自带独立 Python 环境 |
| 脚本中 `python3 -m yt_dlp` 调用失败 | pip 安装的旧版 yt-dlp 与 brew 安装的新版不一致 | 脚本已修改为直接调用 `yt-dlp` 命令（brew 安装的版本） |
| 视频上传乐享报"不支持的文件格式" | 旧版 COS API（`/kb/files/upload-params`）不识别视频格式 | 通过 lexiang MCP 工具使用三步上传流程：`file_apply_upload` → `curl PUT` → `file_commit_upload` |
| Whisper 转录速度极慢 | 模型太大或音频太长 | 换用 `tiny` 或 `base` 模型；对于长视频（>1h），考虑用 `--whisper-model tiny` 先快速预览 |
| 翻译结果为空 | 未设置 `OPENAI_API_KEY` 环境变量 | `export OPENAI_API_KEY=sk-xxx`；或使用 `--skip-translate` 跳过翻译，由 AI 助手在对话中直接翻译全文后用 `md_to_page.py --entry-id` 更新乐享文档 |
| 中英对照格式段落错位 | AI 翻译返回的段落数与原文不匹配 | 脚本已有容错处理（缺少翻译的段落会跳过），可手动补充翻译 |
| 视频上传乐享超时 | 视频文件过大（>500MB）| 使用 MCP 的 `file_apply_upload` 预签名 URL 方式上传，518MB 文件约 30-60 秒即可完成 |
| Whisper 中文转录输出繁体字 | Whisper base 模型对中文普通话倾向输出繁体 | 用 `opencc-python-reimplemented` 的 `t2s` 模式进行繁简转换：`opencc.OpenCC("t2s").convert(text)` |
| 小宇宙播客下载提示 generic extractor | yt-dlp 没有小宇宙专用 extractor | 正常现象，generic extractor 能自动从页面提取音频直链（`media.xyzcdn.net`），下载完全正常 |
| 微信文章图片丢失 | `web_fetch` 无法触发懒加载和绕过防盗链 | **首选**：使用 `file_create_hyperlink` 直接导入（乐享后端自动处理图文）。**降级**：使用 `fetch_article.py`（脚本自动检测微信域名并启用专用处理策略） |
| 乐享知识库操作失败 | MCP 连接异常或 Token 过期 | ① 确认当前 Agent 的 lexiang MCP 已连接（CodeBuddy 检查 MCP 面板、OpenClaw 检查 skill 安装状态）；② Token 过期时访问 https://lexiangla.com/mcp 获取新 Token 并更新 MCP 配置 |
| 文件上传到了知识库根目录而非日期目录 | 跳过了步骤 2（创建日期目录）和步骤 3（去重检查），直接以 `root_entry_id` 作为 `parent_entry_id` 上传 | 严格按照步骤 1→2→3→4 顺序执行，步骤 2 中先 `entry_list_children` 检查日期目录是否存在，不存在则创建 |
| 展示给用户的乐享链接无法访问 | 使用了 MCP API 域名 `mcp.lexiang-app.com` 或缺少 `company_from` 参数 | 所有展示给用户的链接必须按 `config.json` 中 `page_url_template` 格式生成：`https://lexiangla.com/pages/<entry_id>?company_from=<company_from>`。**company_from 不可省略**，否则用户无法访问 |
| PDF 中缺少标题 | `fetch_article.py` 的 `processNode` 将正文 `<h1>` 转为 `# 标题`，与手动拼接的元信息头标题重复；某些网站（如 Lenny's Newsletter）标题在 `articleEl` 外部导致 MD 文件第一行 `# ` 为空 | 已修复：(1) `processNode` 中自动去重正文中与已提取 title 相同的第一个 h1 (2) 标题提取增加 `og:title`、`meta[name="title"]`、`document.title` 多策略回退 (3) `md_to_pdf.py` 增加标题回退——当 MD 中无有效 h1 时从 `article_meta.json` 补充 |
| PDF 中缺少子标题 | 某些网站的 HTML 结构导致 `### # 从 Tab 到 Agents` 被拆为两行：`### #` 和 `从 Tab 到 Agents`，`parse_markdown` 将 `#` 视为无效标题丢弃 | 已修复：`parse_markdown` 增加拆行标题检测——当标题文字为 `#` 或空时，检查下一行是否为实际标题文字并合并 |
| md_to_page.py 导入后文字显示为 base64 乱码 | 脚本通过 HTTP JSON-RPC 直连乐享 MCP API 时，对 content 做了多余的 base64 编码。乐享 MCP 的 base64 要求仅针对 IDE 侧 MCP 协议 | 已修复：去掉 `import_content` 函数中的 `base64.b64encode()`，直传原始 markdown。⚠️ 通过 HTTP JSON-RPC 直连时**永远不要做 base64 编码** |
| md_to_page.py 批量插入图片 block 失败 | `block_create_block_descendant` 一次传多张图片的 descendant 数组会超时或报错 | 改为逐张插入，每次只传一个 image block 的 descendant + children |
| Gemini API 调用报 404 模型不存在 | `gemini-2.0-flash` 模型已下线 | 使用 `gemini-2.5-flash` 替代。可通过 `curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"` 查看当前可用模型 |
| 英文文章未翻译就归档 | 跳过了步骤 3.5 的语言检测和翻译 | **所有英文文章必须翻译为中英对照后再归档**，这是强制步骤不可跳过。🥇 默认用当前模型逐块翻译；🥈 仅用户明确要求且有 `GEMINI_API_KEY` 时用 `translate_gemini.py`。翻译完用 `md_to_page.py --entry-id` 覆盖更新 |
| `translate_gemini.py` 报错 FileNotFoundError | 脚本硬编码了源文件路径，不读取命令行参数 | 已修复：改用 `sys.argv[1]` 读取输入文件，`sys.argv[2]` 读取输出文件，默认输出 `_translated.md` |
| `md_to_page.py` 执行报错 IndentationError | 添加 `--evaluation`/`--evaluation-file` 参数时缩进不一致 | 已修复：参数定义须与上方 `--base-url` 对齐；Python 严禁混用 tab 和空格 |
| `fetch_article.py` 下载的图片在 `md_to_page.py` 中提示 NOT FOUND | 下载保存的文件名与写入 Markdown 的引用不一致（如 `img_06_1c1cfc4c.gif` vs `img_06_1c1cfc42.gif`）| `fetch_article.py` 的 `process_images` 函数中，保存到 `images/` 的文件名与替换 Markdown `src` 时的文件名必须完全一致；建议统一使用 `hash[:8]` + 原始扩展名，并在替换后打印映射表方便排查 |
| 乐享 MCP 更新 token 后工具仍报 "not found" | `mcp.json` 配置已更新，但 MCP 服务未重新加载 | **必须重启 WorkBuddy**（或禁用再重新启用 MCP 服务），新的 token 才能生效 |
| `md_to_page.py` 新增评价信息功能 | 需要在文档顶部插入用户评价（callout 组件）| 已添加 `--evaluation`（短文本）和 `--evaluation-file`（文件路径）两个参数；评价内容会以 blockquote 格式插入文档顶部，乐享会自动渲染为 callout 组件 |
| 播客文字稿章节标题重复出现几十次 | 在 Whisper segment 级别（1-5秒粒度）插入章节标题，且用宽松时间容差匹配 `abs(start - ts) < 5`，导致多个 segment 都命中同一标题 | **必须先合并 segments 为段落（gap<2s, duration<60s），再在段落级别插入标题**。用 `inserted_headers = set()` 跟踪已插入标题，每个标题只插入一次 |
| 日期目录重复创建 | 直接调用 `entry_create_entry` 而不先查询目录是否已存在 | **必须先用 `entry_list_children` 查询根目录**，匹配到同名 folder 则复用其 ID，不存在才创建。已在步骤 2 中加强约束 |
| 得到文章转存后无图片 | 只导入了纯文字，未执行图片上传步骤 | 得到文章**必须**在文字导入后，逐张上传 >50KB 的关键图片（概念图/流程图/配图），流程：`block_apply_block_attachment_upload` → `curl PUT` → `block_create_block_descendant`(image block)。详见"得到 APP 文章抓取"章节 |
| 图片上传后显示不出来 | `block_create_block_descendant` 的 image block 未正确传入 session_id | image block 的 `session_id` 必须来自同一个 `block_apply_block_attachment_upload` 返回值，且 curl PUT 必须返回 HTTP 200 才表示文件上传成功 |
| `fetch_article.py` 抓取 Webflow SPA 站点（如 claude.com）正文为空 | 旧版通用选择器列表中无 Webflow 容器，且内嵌 `<style>` 标签污染提取 | 已修复：`fetch_article.py` 内置 `_is_webflow_blog()` 检测，自动使用 `.u-rich-text-blog` / `.w-richtext` 选择器，并在提取前移除内嵌 `<style>` 标签。无需使用独立脚本 |
| `md_to_page.py` 无法匹配某些图片引用 | 旧版 img_pattern 只匹配 `img_XX_HASH.ext` 格式（fetch_article.py），不匹配其他命名格式 | 已修复：img_pattern 改为通用 `!\[[^\]]*\]\(images/([^)]+)\)`，兼容所有图片命名格式 |
| 新建目录排到末尾而非顶部 | `md_to_page.py` 和手动调用 `entry_move_entry` 时使用 `after=<第一个条目ID>`（排第二）或 `after=""`（排末尾） | 已修复：统一使用 `before=<第一个条目ID>` 实现真正置顶。`after=""` 的 API 文档描述不准确，实测是排末尾 |
| images/ 有图片但乐享文档无图片 | `entry_import_content` 导入 Markdown 时，本地 `![](images/xxx)` 引用不会自动上传图片 | `entry_import_content` 只处理文字，**不会上传本地图片**。有本地图片必须走 `md_to_page.py`（自动处理图文）或降级方案 A（**交替导入**文字和图片，严禁先全文后补图）。步骤 4 开头的「图片判断 Checklist」是必查项 |
| `entry_import_content_to_entry` 中用 `![alt](url)` 或 `<image src="url"/>` 插图后页面显示空白 | 这两种语法在 `entry_import_content` / `entry_import_content_to_entry` 中会产生**空图片 block**（type=image 但无 file_id），页面显示为空白占位符而非实际图片 | **🚨 绝对禁止**在 `entry_import_content` / `entry_import_content_to_entry` 的 content 中使用任何图片语法！图片只能通过 block 级 API 上传：`block_apply_block_attachment_upload`(获取 session_id) → `curl PUT` 上传到 COS → `block_create_block_descendant`(block_type=image, image.session_id)。如果已产生空图片 block，先用 `block_delete_block` 删除，再用 `block_create_block_descendant` 重新创建（`block_update_block` 不支持更新 image 的 session_id/file_id） |
| 图片全部堆积在文档末尾 | 先一次性导入全部文字，事后用 `index=-1` 补图 | **必须交替导入**：按 `![](images/xxx)` 位置拆分 Markdown 为 segments，先导入一段文字 → 上传图片（index=-1 追加到末尾，此时末尾就是正确位置）→ 导入下一段文字 → 上传下一张图片... 详见降级方案 A 的执行流程 |
| Whisper/torch 报 `code signature invalid` 错误 | 沙箱环境对 native `.dylib`/`.so` 做 code signing 校验，`torch` 的 C 扩展无法通过校验 | **禁止静默降级！** 向用户说明情况并申请 `dangerouslyDisableSandbox: true` 权限，在沙箱外执行 Whisper 转录。仅当用户明确拒绝时才可降级为 shownotes/自动字幕方案 |
