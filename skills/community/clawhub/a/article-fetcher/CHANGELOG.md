# Changelog

## v1.3.6 (2026-08-08)

### 🔒 安全修复（基于 ClawHub SkillSpector 审计）

- **P0 — lxml XXE 漏洞（High）**：`requirements.txt` 中 `lxml==6.0.4` → `lxml==6.1.0`，修复 CVE-2026-41066（`iterparse` / `ETCompatXMLParser` 默认配置 XXE）。经核查代码未使用 lxml 解析不可信 XML（MHTML 走 `email` 库、HTML 走 `BeautifulSoup('html.parser')`），升级即消除风险面。
- **P1 — 校正误导性「零网络外发」声明（Medium, Intent-Code Divergence）**：删除 README / SKILL 中「Obsidian 数据完全本地 / 零网络外发 / 不经过网络」等绝对化表述，统一为「Obsidian `.md` 本地落盘 + 文章图片上传阿里云 OSS（必需）」的准确描述。
- **P2 — LLM 外发声明补强（Medium, External Transmission）**：在 `utils/tag_extractor.py` 的 LLM 调用处补充安全注释（可选触发 / endpoint 来自 `LLM_BASE_URL` 配置 / 仅外发前 12000 字符）；README 安全说明新增 LLM 文本外发条目，SKILL `securityNote` 同步声明。
- **P3 — 删除「绕过安全拦截」笔记**：移除 `references/tirith-blocking.md`（审计报告指出的 bypass-prior-blocking 笔记），并确认无其它文件引用。

## v1.3.5 (2026-08-08)

### ✨ 离线输入（HTML / MHTML）

- **新增 `fetchers/offline_parser.py`**：将 HTML 文本 / `.mhtml` 文件解析为标准 `article_data`，复用既有后半段管线（OSS 上传 → 替换 URL → 打标 → 字数 → Obsidian/Notion 归档）
- **`main.py` 抽出 `process_and_archive(article_data, platform, url, tags)`**：URL 抓取与离线输入共用同一归档流程，行为零变化
- **新增离线入口**：`archive_from_html()` / `archive_from_mhtml()`
- **CLI 扩展（`sys.argv` 手动解析，不使用 argparse，遵循安全合规约定）**：`--html`（支持 `-` 读 stdin）/`--mhtml`/`--platform`（默认 wechat）/`--url`（可选）
- **三陷阱修复（源自 wechat-article-capture 技能沉淀）**：
  - 微信懒加载：`data-src`→`src` 并 `del data-src`，根治 markdownify 读占位符
  - MHTML 编码：`get_payload(decode=True)` 取 bytes 后按 `get_content_charset()` 或 `utf-8` 解码，避免乱码
  - `data:image/svg+xml` 占位符过滤，图片列表归一化（去 query、去重）确保 URL 替换可命中

### 🔧 本地适配

- **Vault 去序号**：存档目录从 `1-收件箱/` 改为 `收件箱/`（知衍库 2026-07 架构调整）
- **移除 `distilled: false`**：蒸馏状态判定已改为文件存在性模型，不再依赖 frontmatter 标记
- **裁撤 `wechat-article-capture` 技能**：v1.3.5 的 MHTML/HTML 离线模式已覆盖其全部功能，无需单独维护

### 🐛 已知问题

- ~~**Notion 转换**：`### | title` 格式标题会被 Notion API 误判为表格分隔符~~ **已修复 (v1.3.5-local)**：根因为 `_parse_inline_html` 将内联 `<img>` 当作 image block 塞入 `rich_text`，导致 `text` 字段缺失。修复为内联图片转文本链接 `[alt](url)`。

---

## v1.3.4 (2026-07-19)

### 🔒 Tirith `requires.env` 补全

- **`NOTION_API_KEY` / `LLM_API_KEY` 加入 `requires.env`**：代码实际读取的可选凭证必须在元数据声明，消除 CRITICAL exfiltration 误报

---

## v1.3.3 (2026-07-06)

### 🔒 Tirith 安全扫描兼容

- **元数据 `allowedEnv` 声明**：显式列出所有读取的环境变量及用途，避免 `NOTION_API_KEY`/`LLM_API_KEY` 被误判为外泄
- **元数据 `securityNote`**：说明凭证用途，OSS 必需，Notion/LLM 可选
- **移除 `pip install` 文本**：代码日志和文档中的 `pip install` 语句替换为 `requirements.txt` 引用，消除供应链误报

---

## v1.3.2 (2026-07-06)

### 🐛 修复

- **文件名补日期前缀**：`_build_filename` 恢复 `{YYYY-MM-DD}_{title}.md` 格式，Obsidian 内按时间线排序
- **图片 Referer 空优先 + 403 回退**：新增 `_download_image()`，先空 Referer 请求，403 时自动回退平台 Referer

---

## v1.3.1 (2026-07-06)

### 🔒 安全审计修复

- **依赖升级**：`lxml` 6.0.2→6.0.4 (CVE-2026-41066 XXE)、`urllib3` 2.0.7→2.7.0 (多项 CVE)
- **权限声明**：SKILL.md metadata 新增 `permissions: [env:read, net:outbound, fs:write]`
- **隐私声明修正**：移除"数据完全本地"误导性表述，明确 LLM 外发范围和图片下载行为
- **安全章节补充**：新增 LLM 外发范围说明、图片下载风险提示

---

## v1.3.0 (2026-07-06)

### 🆕 微信 Playwright 回退 + 空内容检测

- **微信二级回退**：`wechat_fetcher.py` 新增 `_fetch_with_playwright()`，HTTP 反爬时自动 Playwright 回退
- **空内容检测**：`_is_valid()` 检测正文为空/反爬关键词，阻止垃圾文件生成
- **图片 Referer 动态化**：`upload_images()` 新增 `article_url` 参数，从原文链接提取 Referer，兼容第三方 CDN

### 🐛 修复

- **文档文件名修正**：SKILL.md 改为 `{title}.md`，与实际输出一致

---

## v1.2.0 (2026-07-05)

### 🆕 知乎 403 二级回退

- **Playwright 浏览器回退**：`zhihu_fetcher.py` 新增 `_fetch_with_playwright()`，HTTP 403 时自动启动 headless Chromium 抓取
- **Cookies 注入**：Netscape Cookies 自动注入到 Playwright 浏览器上下文
- **二级策略**：HTTP (Cookies) → Playwright → 失败放弃（不生成垃圾文件）
- **`_parse()` 提取**：HTTP 和 Playwright 两条路径复用同一解析逻辑
- **Playwright 渲染等待**：`page.goto()` 后新增 `wait_for_timeout(3000)`，解决页面未渲染完就取内容报错
- **Pin 类型支持**：新增 `_extract_pin()` 方法，支持知乎想法（`/pin/`）解析，含图片懒加载修复

### 🐛 修复

- **ObsidianArchiver 无参构造**：`__init__` 改为可选 `vault_path` 参数，兼容各种调用场景
- **图片懒加载**：_extract_pin 中将 `data-original`/`data-actualsrc` 回填到 `src`，避免 OSS 替换时失配

### 📝 文档

- SKILL.md / README.md 新增知乎 403 回退策略说明
- metadata 新增 `playwright install chromium` 安装步骤

---

## v1.1.0 (2026-06-22)

### 🆕 Obsidian 本地存档

- **新增 `obsidian_archiver.py`**：HTML → Markdown 转换（`markdownify`），YAML Frontmatter，存入 `1-输入-收件箱/文章收藏/`
- **4 场景存档调度**：Obsidian 优先 / Notion 可选 / 双写 / 仅预览
- **`config.py` 重构**：Notion 移出必需校验，新增 `obsidian_available` / `notion_available` / `archive_available` 属性
- **文件名简化**：仅保留标题，去除日期前缀

### 🐛 修复

- **OSS URL 双协议头防御**：`image_processor.py` endpoint 前置 `lstrip` 处理
- **小红书 JSON 提取**：`xhs_fetcher.py` 改用 `html.unescape()` + `get_text()` 防 BS4 转义破坏 JSON
- **HTTP Session 复用**：`http_client.py` 改为模块级单例 + 连接池
- **微信图片空白**：`main.py` 新增 `data-src` → `src` 修复，解决懒加载图片在 Markdown 中丢失
- **`__init__.py` 恢复**：5 个子包补回 `__init__.py`，解决包导入失败

### 🔧 优化

- **`.env` 加载策略**：`$AGENT_HOME` > `$HERMES_HOME` > 当前目录，agent 无关通用方案
- **标签 Obsidian 兼容**：`tag_extractor.py` LLM prompt 约束 + 统一清洗空格→`-`
- **跨平台路径示例**：文档中 `OBSIDIAN_VAULT_PATH` 展示 Windows/macOS/Linux 三平台

### 📝 文档

- **SKILL.md / README.md 全面重写**：4 场景存档表、Obsidian Frontmatter 规范、Notion 降级为可选
- `openclaw` metadata → `hermes`，路径 `~/.hermes` → `$AGENT_HOME`

---

## v1.0.2 (2026-05-10)

### 🏗️ LLM 多平台抽象

- **统一 LLM 配置**：`config.py` 移除 DashScope 专属字段（`dashscope_api_key`/`dashscope_base_url`/`dashscope_model`），改为 `LLM_API_KEY` + `LLM_BASE_URL` + `LLM_MODEL` 通用配置
- **复用 video-summarizer 配置**：LLM 三个环境变量与 video-summarizer 共享 `.env`，无需重复设置
- **重构 `tag_extractor.py`**：`extract_tags_llm()` 改为 OpenAI 兼容接口，支持 DeepSeek / DashScope / OpenAI / Groq 等任意平台
- **LLM 可用性标记**：config 新增 `llm_available` 属性，一次判断即可决定是否启用 LLM
- **升级日志**：LLM 调用增加模型名称打印（如 `deepseek-v4-pro`），便于排错

---

## v1.0.1 (2026-05-07)

### 🔒 安全修复（ClawScan 扫描）

- **Cookie 域隔离**: `base_fetcher.py` 重构 `_load_cookies()` 保留 domain 字段，新增 `_apply_cookies_for_url(url)` 按目标域名过滤，防止登录态泄露到非目标站点
- **URL 严格校验**: `platform_detector.py` 改用 `urllib.parse.urlparse` + 白名单匹配 hostname，拒绝路径拼接攻击（如 `https://evil.com/mp.weixin.qq.com/...`）
- **依赖版本锁定**: `requirements.txt` `>=` → `==` 精确版本，降低供应链风险

### 📝 文档

- **安全说明**: SKILL.md 新增「安全与隐私」章节，披露 LLM 数据外发、Cookie 隔离、权限最小化等安全边界
- **扩展指南**: 更新平台扩展步骤（`ALLOWED_HOSTS` 替换旧正则描述）

---

## v1.0.0 (2026-05-07)

### 🎯 正式发布

- **文档精简**: SKILL.md 重写为精简扼要格式，层次清晰，面向用户与 Agent
- **版本标注**: 统一版本号为 v1.0.0（SKILL.md metadata、README、CHANGELOG）
- **清理冗余**: 移除 `tests/` 目录、`__init__.py`、`__pycache__/` 缓存文件
- **安全加固**: 消除 `config.py` 中 `DEBUG` 变量暴露到全局模块命名空间
- **SKILL.md**: 新增 Notion 数据库字段说明、扩展平台指南、模块调用示例

---

## v0.2.0 (2026-05-06)

### ✨ 关键词提取优化

- **LLM 优先策略**: 关键词提取优先调用 DashScope LLM 理解文章核心内容
- **智能降级**: LLM 失败或未配置 `DASHSCOPE_API_KEY` 时自动降级为本地词频分析
- **标题上下文**: 传递文章标题给 LLM，提升关键词提取准确度
- **超时重试**: 3 次重试机制（60s → 90s → 120s），兼容 429/5xx 错误
- **新增配置**: `.env.example` 添加 `DASHSCOPE_API_KEY`/`DASHSCOPE_BASE_URL`/`DASHSCOPE_MODEL` 说明

### 📝 文档更新

- SKILL.md 更新关键词提取描述（纯本地 → LLM 优先 + 降级方案）

---

## v0.1.1 (2026-05-01)

### 🐛 Bug 修复

- **关键词提取**: 移除 LLM API 依赖，改为纯本地词频方案，解决 Coding Plan Key 不能用于后端脚本的合规问题
- **知乎抓取**: 修复 `#HttpOnly` 前缀导致 Cookies 解析失败（base_fetcher.py）
- **知乎清理**: 移除知乎 HTML 中 64K+ CSS 噪音（内嵌 `<style>` 标签、动态 class、JS 属性）
- **知乎图片提取**: 修复图片选择器不匹配问题，提取 `_r.jpg` + `_720w.jpg` 双变体 URL
- **Notion 存档**: 修复单段文本超过 2000 字符导致 400 错误，段落/引用/代码块自动拆分
- **Notion 图片**: 修复知乎图片 SVG 占位符未被跳过的问题，增加 `data-original` 优先级

### 🔧 优化

- **Cookies 路径**: 默认路径改为 `~/.cookies/<platform>_cookies.txt`，可通过环境变量覆盖
- **安全文档**: SKILL.md 新增完整的「安全与隐私说明」章节
- **SKILL.md**: 更新关键词提取描述（LLM → 纯本地词频）

---

## v0.1.0 (2026-04-29)

### ✨ 初始版本

- 多平台支持：微信公众号、小红书、豆瓣、知乎
- 图片上传阿里云 OSS
- 关键词提取（LLM + 词频降级方案）
- 一键存档到 Notion
