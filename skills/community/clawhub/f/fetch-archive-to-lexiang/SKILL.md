---
name: fetch-archive-to-lexiang
version: "2.8.2"
author: ajaxhe
license: MIT
category: research
description: Fetch paywalled articles (Substack/Medium), transcribe YouTube & podcasts, extract & translate PDFs. Archive to Lexiang knowledge base. 抓取付费文章、YouTube/播客转录、PDF翻译归档，转存乐享知识库。
tags: fetch, archive, youtube, podcast, pdf, transcribe, lexiang, paywall, substack, medium, arxiv, weibo, chinese
disable-model-invocation: false
requires:
  mcp:
    - lexiang
  binaries:
    - python3
    - yt-dlp
  python:
    - playwright
    - pymupdf
    - openai-whisper
---

# 抓取链接内容 & 转存知识库

## 核心规则

1. **文件命名**：必须用原文标题命名（`<标题>.md`），不用 `article.md`
2. **原文链接必须保留**：确保读者可以追溯原始出处。根据文档类型采用不同方式：
   - **可编辑文档**（在线文档/Markdown页面）：在文档标题下方、作者信息上方插入 `**原文链接**：[文章标题](原始URL)`
   - **不可编辑文件**（视频、音频、PDF等）：上传后通过 `knowledge_tag_set_entry_tags` 或 `comment_list_comments` → 评论方式附上原文链接
3. **乐享链接格式**：按步骤 0 读取的 `access_domain.page_url_template` 生成（禁止 `mcp.lexiang-app.com`，禁止硬编码 company_from）
4. **非中文内容必须翻译**：中英对照格式（每段英文后紧跟中文翻译）
   - **翻译执行方式**：🥇 **默认用当前运行 skill 的大模型（Agent 自己）逐块翻译**；🥈 仅当用户**明确要求**用 Gemini **且**已提供 `GEMINI_API_KEY` 时，才用 `scripts/translate_gemini.py`
   - **🚨 标题必须单行双语**：`## English Title / 中文标题`（英文中文同一行用 ` / ` 分隔），**禁止把中文译文另起一行变成独立标题**——否则一个章节在目录里占两行，目录极不便查看
   - **🚨 标题层级要克制，避免目录膨胀**：只给真正的章节/小节设标题。作者名、人物叙事名、重复的子标签（如「The posture / The tradeoff」）、纯数字/百分比等**一律用加粗正文**（`**...**`），不设标题；同一大章节的要点用一行列表表达，不要每条都拆成标题
5. **图片不可丢失**：有图片的文章必须用 `fetch_article.py` 抓取 + `md_to_page.py` 导入（或 MCP Direct HTTP Call 降级方案）
6. **🚨 翻译必须保留图片语法**：中英对照翻译时，原文的 `![alt](images/xxx)` 图片引用**必须原样保留在对应位置**，禁止替换为 `[IMG_PLACEHOLDER_N]` 或任何非标准占位符。`md_to_page.py` 依赖 `![](...)` 语法来拆分文本和图片段——占位符会导致图片语法无法被识别，被迫走 MCP 手动定位路径（index 不可靠），最终图片错位或缺失
7. **🚨 全自动执行，禁止不必要的用户确认**：当首选方法（如 `md_to_page.py`）因缺少 LEXIANG_TOKEN 等原因不可用时，Agent 必须**自动切换到降级方案**（MCP Direct HTTP Call）并完成全部操作（包括图片上传），**禁止停下来问用户「是否要继续上传图片？」或「是否要我继续？」**。只有在所有方法都失败时才向用户报告错误。详见 Step 3「MCP 直接调用方法」章节

## 工作流程总览

```
Step 0: 🔍 预检（读取自省日志 + 侦察原文）  ← 新增！每次必做
Step 1: 素材收集（抓取原文+图片）
Step 2: 语言检测 → 非中文则翻译为中英对照
Step 3: 转存到乐享知识库（日期目录 + 图文导入）
Step 4: ✅ 交付自检（对照清单逐项验证）      ← 新增！每次必做
Step 5: 📝 自省（有问题则更新 lessons-learned.md）
```

## Step 0：预检（🚨 每次任务开头必做，不可跳过）

**0a. 读取自省日志**
- 读取 [references/lessons-learned.md](references/lessons-learned.md) 中的 🔴 P0 教训
- 将 P0 教训作为本次执行的「红线清单」，在后续每个决策点主动对照

**0b. 侦察原文**
- 用 `WebFetch` 快速扫描原文，**明确记录**以下信息：
  - 文章标题、作者、日期
  - 📸 **是否包含图片？有几张？** ← 这是最容易遗漏的！
  - 文章语言（中文/英文/其他）
  - 文章长度（短/中/长）
  - 是否有付费墙/登录墙
- 基于侦察结果，**在开始抓取前向用户确认执行计划**：
  ```
  📋 预检报告：
  - 标题：（预检后填入实际标题）
  - 语言：英文 → 需翻译为中英对照
  - 图片：发现 N 张配图 → 将使用 fetch_article.py 抓取
  - 预计上传方式：md_to_page.py（含图片）
  ```

**0c. 抓取方式决策**
- 有图片 → **必须**用 `fetch_article.py`，**禁止**仅用 WebFetch
- 无图片 + 无付费墙 → 可用 WebFetch 内容直接导入
- 有付费墙 → `fetch_article.py --cdp`

## Step 1：素材收集（抓取方式决策树）

根据 URL 类型选择抓取方式（按优先级）：

| 优先级 | URL 类型 | 抓取方式 | 详细参考 |
|--------|----------|----------|----------|
| 1 | 微信公众号 `mp.weixin.qq.com` | 乐享 MCP `file_create_hyperlink` 一步到位 | [platform-specific.md](references/platform-specific.md) |
| 2 | YouTube 视频 | `scripts/yt_download_transcribe.py` | [youtube-video.md](references/youtube-video.md) |
| 2b | 含嵌入视频/播客的文章（Substack/Newsletter 等） | 提取 YouTube 链接 → `yt_download_transcribe.py` | [youtube-video.md](references/youtube-video.md) |
| 3 | 播客音频（小宇宙等）| `scripts/podcast_to_lexiang.py`（**Show Notes + 转录**） + 标题文件夹归档 | [podcast-audio.md](references/podcast-audio.md) |
| 4 | **PDF（乐享内条目 / 直链 / 本地）需翻译+富排版** | **组合 `pdf-rich-translate` skill** 做提取/裁剪/翻译/富元素标注 → 本 skill 归档 | [pdf-processing.md](references/pdf-processing.md)（归档侧） + `pdf-rich-translate` |
| 5 | 付费/登录墙文章 | `scripts/fetch_article.py`（Cookie/CDP） | 见下方 |
| 6 | 免费图文文章 | `scripts/fetch_article.py` | 见下方 |
| 7 | 得到 APP | `fetch_article.py --cdp` | [platform-specific.md](references/platform-specific.md) |
| 8 | SPA 动态网站 | Playwright 生成 PDF | [platform-specific.md](references/platform-specific.md) |

### fetch_article.py 用法

```bash
# 标准模式（Cookie 注入）
python3 scripts/fetch_article.py fetch "<URL>" --output-dir <项目子目录>

# CDP 模式（Substack/微博/Cloudflare 等需要完整登录态的站点）
python3 scripts/fetch_article.py fetch "<URL>" --output-dir <项目子目录> --cdp
```

**CDP 模式说明**：

脚本会**自动**完成 Chrome 启动与 Cookie 同步，无需手动操作：
1. 检测 `127.0.0.1:9222` 是否已有 Chrome 运行 → 有则直接复用
2. 没有则自动启动 Chrome，使用永久 CDP Profile：`~/.fetch_article/chrome_cdp_profile`
3. 自动将用户日常 Chrome 的 Cookies 同步到 CDP Profile（大多数已登录网站无需重新登录）

**永久 CDP Profile 设计原则**：

```
日常 Chrome                        CDP Chrome（抓取专用）
~/Library/.../Chrome/Default       ~/.fetch_article/chrome_cdp_profile
（历史、书签、密码）                （独立 Profile，脚本自动管理）
                                            ↑
                                   每次启动前自动同步日常 Chrome Cookies
```

- 两个 Chrome 可同时运行，**互不影响**
- CDP Profile 是永久目录（非 `/tmp`），登录状态跨会话保留
- 付费网站（如 SemiAnalysis）首次在 CDP Chrome 中手动登录一次，后续永久复用

**手动启动 CDP Chrome（当脚本无法自动启动时）**：

> 在 Cursor 环境中，Agent 的 Shell 进程结束时子进程会被一并终止。遇到此情况，用以下命令通过 macOS Launch Services 启动（完全独立于 Shell 生命周期）：

```bash
# 使用永久 CDP Profile（不会丢失登录状态）
open -a "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.fetch_article/chrome_cdp_profile" \
  --no-first-run --no-default-browser-check

# 或使用快捷脚本
~/.fetch_article/start-cdp-chrome.sh
```

> 🚫 **禁止**使用 `/tmp/chrome-cdp-profile`（临时目录，重启后登录状态全失）

**产出物**：
- `<项目子目录>/<标题>.md` — Markdown 正文
- `<项目子目录>/<标题>_meta.json` — 元信息
- `<项目子目录>/images/` — 配图

> ⚠️ `web_fetch` 无法下载图片。有图片的文章**必须**用 `fetch_article.py`。

## Step 2：语言检测与翻译

读取抓取内容前 500 字符，统计中文字符占比：
- ≥ 30% → 中文，跳过翻译
- < 30% → 非中文，**必须翻译为中英对照格式**

**翻译执行方式**：🥇 默认用当前运行 skill 的大模型（Agent 自己）逐块翻译（长文按 3000–5000 字符分块）；🥈 仅当用户明确要求且提供 `GEMINI_API_KEY` 时才用 `scripts/translate_gemini.py`。

中英对照格式：每段先英文原文，紧跟中文翻译。文档顶部格式为：
```
# 文章标题 / 中文标题
**原文链接**：[文章标题](原始URL)

*By Author · Date · Platform*
```

🚨 **标题规则（直接影响乐享目录质量）**：
- **单行双语**：`## English Title / 中文标题`（同一行 ` / ` 分隔），**禁止**中文译文另起一行成为独立标题（否则目录里一个章节占两行）
- **层级克制**：只给真正的章节/小节设标题；作者名、人物名、重复子标签、纯数字百分比等用加粗正文 `**...**`，不设标题，避免目录膨胀

🚨 **图片语法保留规则（翻译时必须遵守）**：
- 原文中的 `![alt](images/xxx)` 图片引用**必须原样保留**，不得替换为 `[IMG_PLACEHOLDER_N]` 或任何非标准格式
- 图片引用应放在对应段落的上方或下方，确保图文对应关系不丢失
- alt 文本可翻译为双语（如 `![Zone of Genius framework / 天才区域框架](images/img_03_xxx.png)`）
- 这条规则是核心规则#6 的具体执行指引，违反会导致 `md_to_page.py` 无法自动处理图片

## Step 3：转存乐享知识库

> 详细的上传步骤、降级方案、图片处理见 [lexiang-upload.md](references/lexiang-upload.md)

### 操作流程（严格按顺序，不可跳步）

**步骤 0：读取目标知识库配置（优先级从高到低）**

```
1. 🗣️  对话上下文（用户本次明确指定，如"转存到 XX 知识库"）→ 直接使用，不读文件

2. 🧠  Agent 工作区记忆（工作区规则文件，含敏感信息，已 gitignore）
       Cursor:  <工作区>/.cursor/rules/fetch-archive-defaults.mdc
       其他:    各 Agent 对应的工作区记忆文件

3. 📄  skill 配置文件（<skill目录>/config.json，已 gitignore，不入 GitHub）

4. ❌  若以上均未找到 → 触发初始化向导（见下方）
```

> 🚨 **安全红线**：`space_id` / `company_from` 等敏感信息**只能**存在于 gitignore 文件或 Agent 记忆中，
> **严禁**写入 SKILL.md 或任何 git 跟踪文件。

**初始化向导（步骤 0 第 4 条触发时执行）**

```
Agent 提示：未检测到目标知识库配置，是否现在初始化？
用户操作：粘贴知识库链接（如 https://lexiangla.com/spaces/xxx?company_from=yyy）
Agent 执行：
  ① 解析 space_id、company_from、domain
  ② space_describe_space 验证可访问性，提取 space_name
  ③ 同时写入两处（缺一不可）：
     - <skill目录>/config.json（已 gitignore）
     - <工作区>/.cursor/rules/fetch-archive-defaults.mdc（需加入工作区 .gitignore）
  ④ 提示「已配置，后续默认转存到「{space_name}」」并继续执行原始任务
```

更新配置：直接告知 Agent "把默认知识库改成 XX"，重复步骤 ③ 覆盖写入两处即可。

**步骤 1：获取知识库根节点**
- `space_describe_space(space_id)` → 提取 `root_entry_id`

**步骤 2：检查/创建日期目录（🚨 先查再建）**

```
2a. entry_list_children(parent_id=root_entry_id, sort_by="sort_id", limit=5)
    → 遍历找 name=="今天日期" 且 entry_type=="folder"
    → 找到 → 复用其 ID
    → 没找到 → 步骤 2b

2b. entry_create_entry(entry_type="folder", parent_entry_id=root_entry_id, name="今天日期")
    
    🚨 创建后必须置顶：
    → entry_list_children(parent_id=root_entry_id, sort_by="sort_id", limit=1) 获取当前第一个条目 ID
    → entry_move_entry(entry_id=新目录, parent_id=root_entry_id, before=第一个条目ID)
    
    ⚠️ after="" 是排末尾（API 文档有误），禁止使用！
    ⚠️ 必须用 before=<第一个条目ID> 才能真正置顶
```

**步骤 3：去重检查**
- `entry_list_children(parent_id=日期目录ID)` → 按名称+类型检查是否已存在

**步骤 4：上传文档**

| 情况 | 方式 |
|------|------|
| 微信公众号 | `file_create_hyperlink`（一步到位，后端自动抓图文） |
| 有图片的文章（✅ 首选） | `scripts/md_to_page.py --parent-id <日期目录ID> --name "标题"`（需 LEXIANG_TOKEN，见下方获取方式） |
| 有图片的文章（🥈 **推荐降级** — 无 LEXIANG_TOKEN 时全自动执行，**无需用户确认**） | **MCP Direct HTTP Call**（直接 HTTP POST 到 LeXiang MCP 端点，详见下方「MCP 直接调用方法」） |
| 有图片的文章（备选 — 通过 DeferExecuteTool 逐工具调用） | MCP connector "先全文后补图"（参数较小时可用，>10K 字符可能截断，见 [lexiang-upload.md](references/lexiang-upload.md)） |
| 纯文本 ≤30K 字符 | `entry_import_content(parent_id, name, content, content_type="markdown")` |
| **纯文本 >30K 字符（大文档）** | **`scripts/upload_doc_to_lexiang.py`** 或 **MCP Direct HTTP Call**（见下方） |
| 视频/音频（仅上传文件） | `scripts/upload_video_via_openapi.py --media-type video/audio` |
| **视频转录归档（文字稿+视频）** | 创建标题文件夹 → 文字稿上传为 file → 视频作为子文档（见 [youtube-video.md](references/youtube-video.md)） |
| **播客转录归档（Show Notes + 文字稿 + 音频）** | 创建标题文件夹 → 文字稿（含节目介绍）上传为 file → 音频作为子文档（见 [podcast-audio.md](references/podcast-audio.md)） |

### 🚨 MCP 直接调用方法（L021 — 无 LEXIANG_TOKEN 时的首选降级方案）

> **核心价值**：当 `md_to_page.py` 因缺少 LEXIANG_TOKEN 不可用时，本方法可**全自动完成图文上传**（创建页面→导入全文→逐张上传图片→插入 block→删除占位符），**无需任何用户确认或介入**。
>
> ⚠️ **🚨 禁止停下来问用户！** 当 md_to_page.py 不可用时，Agent 应直接使用本方法完成全部操作。只有在所有方法都失败时才向用户报告错误。

**Token 获取**（WorkBuddy/Cursor 环境）：

```bash
# WorkBuddy：从 connector 配置中提取
grep -r "connector.*lexiang" ~/.workbuddy/connectors/*/mcp.json | head -1
# → 找到 mcp.json 路径后：
python3 -c "import json; d=json.load(open('找到的mcp.json路径')); print(d['mcpServers']['connector:lexiang']['headers']['Authorization'])"

# Cursor：从 MCP 配置中提取（格式可能含 Bearer 前缀）
python3 -c "import json; d=json.load(open('$HOME/.cursor/mcp.json')); print(d['mcpServers']['lexiang']['headers']['Authorization'].replace('Bearer ',''))"
```

**完整图文上传流程（Phase A → Phase B → Phase C）**：

```
═══ Phase A: 创建页面 + 导入全文 ═══

A1. entry_create_entry(entry_type="page", parent_id=<日期目录ID>, name="标题")
    → 获得 page_entry_id

A2. 准备纯文字版 markdown：
    - 读取 article_bilingual.md（中英对照版）
    - 将 ![xxx](images/yyy) 替换为 [图片 N: yyy] 占位标记
    - 得到 article_text_only.md

A3. 通过 HTTP POST 调用 entry_import_content 导入全文：

    Python 调用模板（可直接在 Bash 中执行）：
    ┌──────────────────────────────────────────────────────┐
    │ import json, urllib.request                            │
    │                                                       │
    │ TOKEN = "<从上面步骤获取的token>"                        │
    │ COMPANY_FROM = "<config中的company_from>"               │
    │ MCP_URL = f"https://mcp.lexiang-app.com/mcp?company_from={COMPANY_FROM}" │
    │                                                       │
    │ # 读取纯文字版内容                                      │
    │ with open("article_text_only.md", "r") as f:           │
    │     content = f.read()                                │
    │                                                       │
    │ mcp_request = {                                       │
    │   "jsonrpc": "2.0", "id": 1,                          │
    │   "method": "tools/call",                             │
    │   "params": {                                         │
    │     "name": "entry_import_content",                    │
    │     "arguments": {                                    │
    │       "parent_id": "<日期目录ID>",                      │
    │       "name": "文档标题",                              │
    │       "content": content,       # 完整内容，14K+ 可一次传入│
    │       "content_type": "markdown",                      │
    │       "space_id": "<SPACE_ID>"                         │
    │     }                                                 │
    │   }                                                   │
    │ }                                                     │
    │                                                       │
    │ req = urllib.request.Request(                          │
    │     MCP_URL,                                          │
    │     data=json.dumps(mcp_request).encode("utf-8"),      │
    │     headers={"Content-Type": "application/json",      │
    │              "Authorization": TOKEN},                 │
    │     method="POST"                                     │
    │ )                                                     │
    │ with urllib.request.urlopen(req, timeout=60) as resp:  │
    │     result = json.loads(resp.read().decode())          │
    │     # 解析响应：result['result']['content'][0]['text'] │
    │     # 是 JSON 字符串，需二次 json.loads()                │
    │     inner = json.loads(result['result']['content'][0]['text']) │
    │     entry_id = inner['data']['entry']['id']            │
    │     print(f"Page created: {entry_id}")                │
    └──────────────────────────────────────────────────────┘

═══ Phase B: 逐张上传图片并插入正确位置（从后往前！） ═══

B1. 获取页面 block 结构：
    调用 block_list_block_children(entry_id, with_descendants=False)
    → 遍历 blocks，找到每个 [图片 N] 占位 block 的 index 和 block_id
    → 记录: [(index_1, block_id_1, img_path_1), ..., (index_N, block_id_N, img_path_N)]

B2. 对每张图片（从后往前处理！避免 index 偏移）：

    对 i from len(images)-1 downto 0:
    ├── b2a. file_apply_upload(
    │        parent_entry_id=entry_id,
    │        name="文件名.png",
    │        size=str(文件字节数),     ← 必须是字符串！
    │        mime_type="image/png|jpeg", ← 用 sips 检测实际格式
    │        upload_type="PRE_SIGNED_URL"
    │      )
    │   → session_id + upload_url
    │
    ├── b2b. 上传到 COS（Python urllib.request，禁止用 curl！）：
    │    with open(img_path, 'rb') as f:
    │        img_data = f.read()
    │    req = urllib.request.Request(upload_url,
    │        data=img_data,
    │        headers={'Content-Type': mime_type,
    │                 'Content-Length': str(len(img_data))},
    │        method='PUT')
    │    with urllib.request.urlopen(req, timeout=60) as resp:
    │        assert resp.status == 200
    │
    ├── b2c. file_commit_upload(session=session_id)
    │   → 返回 entry.target_id (= file_id)
    │
    └── b2d. 在占位位置插入 image block：
         block_create_block_descendant(
           entry_id=entry_id,
           index=str(占位block的index),   ← 必须是字符串！
           descendant=[{
             "block_id": f"temp_img_{i}",
             "block_type": "image",
             "image": {"session_id": session_id}
           }]
         )

B3. 删除所有占位 block（从后往前删除！）：

    for each placeholder_block_id (从后往前):
        block_delete_block(block_id=placeholder_block_id, entry_id=entry_id)
        🚨 必须传 entry_id 参数！

═══ Phase C: 验证 ═══

C1. block_list_block_children(entry_id)
    → 统计 block_type=="image" 的数量 == 原图数量？
C2. 检查无残留 [图片 N] 占位 text block？
C3. 输出乐享链接 + 交付自检清单
```

**⚠️ 关键注意事项**：

1. **不要停下来问用户！** 当 md_to_page.py 不可用时，直接执行上述流程，不要输出「是否要继续将图片上传到乐享？」之类的确认提示
2. MCP JSON-RPC 响应需要二次解析：`json.loads(response['result']['content'][0]['text'])`
3. `file_apply_upload` 的 `size` 必须是字符串 `"12345"` 不是整数
4. `block_create_block_descendant` 的 `index` 必须是字符串 `"13"` 不是整数
5. `block_delete_block` 必须传 `entry_id`
6. COS 上传必须用 Python `urllib.request`（curl 会因 URL 特殊字符 %2F/%3B 等返回 403）
7. 从后往前处理图片和删除占位符，避免 index 偏移
8. 图片 MIME 类型必须匹配实际格式（`.png` 扩展名的文件可能是 JPEG，用 `sips -g format` 检测）

**适用场景优先级总结**：

```
有图片文章的上传路径选择：
┌─ md_to_page.py (LEXIANG_TOKEN 可用)          → 🥇 首选，一步到位
├─ MCP Direct HTTP Call (本文档方法)            → 🥈 推荐降级，全自动
├─ DeferExecuteTool + call_tool 包装器           → 🥉 备选，参数较小时可用
└─ .md 文件上传 (最终降级)                       → 仅当前两者都失败时
```

**🚨 大文档上传策略（>30K字符）**：

Agent **禁止**通过 MCP 工具参数直接传入大段 content（会超限失败 + 上下文腐化）。

```bash
# 有 LEXIANG_TOKEN 时（最佳，创建在线文档）：
python3 scripts/upload_doc_to_lexiang.py <文件.md> \
    --parent-id <目录ID> --name "标题" --space-id <SPACE_ID>

# 无 LEXIANG_TOKEN 时（Agent 执行 3 步操作）：
python3 scripts/upload_doc_to_lexiang.py <文件.md> \
    --parent-id <目录ID> --name "标题" --mode instructions
# → 输出 JSON 指令，Agent 按指令执行 file_apply_upload → curl PUT → file_commit_upload
```

**LEXIANG_TOKEN 获取方式**：

```bash
# 方式一（推荐）：直接从 Cursor MCP 配置读取（Cursor 会自动维护此 token）
python3 -c "import json; d=json.load(open('$HOME/.cursor/mcp.json')); print(d['mcpServers']['lexiang']['headers']['Authorization'].replace('Bearer ',''))"

# 方式二：访问 https://lexiangla.com/mcp 手动获取（格式：lxmcp_xxx）
```

> ⚠️ **LEXIANG_TOKEN 有效期约 2 小时**，过期后 `md_to_page.py` 的图片上传全部失败（401）。每次使用 `md_to_page.py` 前，先用方式一从 `~/.cursor/mcp.json` 读取最新 token。MCP connector 方式不受 token 过期影响，可作为兜底。

## 脚本文件

| 脚本 | 用途 |
|------|------|
| `scripts/lexiang_pdf_parse.py` | **读取乐享内 PDF 原文**：调用 `entry_describe_ai_parse_content` 拿完整解析 markdown + 图片清单 + 元信息（含转存目标 `parent_id`），可选下载原 PDF |
| `scripts/upload_doc_to_lexiang.py` | **通用大文档上传**：绕过 MCP 参数限制，支持在线文档/文件两种模式 |
| `scripts/podcast_to_lexiang.py` | **播客全流程**：下载→抓取Show Notes→FunASR转录→Markdown→上传 |
| `scripts/fetch_article.py` | 抓取文章（Cookie/CDP/Substack） |
| `scripts/md_to_page.py` | Markdown + 图片 → 乐享在线文档（需 LEXIANG_TOKEN） |
| `scripts/yt_download_transcribe.py` | YouTube 下载 + Whisper 转录 + 翻译 |
| `scripts/upload_video_via_openapi.py` | 视频/音频上传到乐享（VOD 路径） |
| `scripts/md_to_pdf.py` | Markdown → PDF（最终降级方案） |

## 关键约束

- 🚨 **沙箱权限与转录降级**：Whisper/torch/faster-whisper 等含 native 库的 Python 包在沙箱环境可能因 code signing 失败。**禁止静默降级**（如用 shownotes 代替逐字转录）！必须先向用户申请沙箱外执行权限（`dangerouslyDisableSandbox: true`），用户同意后再执行；仅当用户明确拒绝时才可降级处理
- 🚨 **视频/音频上传**必须用 `upload_video_via_openapi.py`（走 VOD），不用 MCP 的 `file_apply_upload`
- 🚨 **日期目录**必须先查再建，创建后必须用 `before` 置顶
- 🚨 **图片处理**贯穿全流程，`entry_import_content` / `entry_import_content_to_entry` **不会上传任何图片**。在 content 中写 `![alt](url)` 或 `<image src="url"/>` 会产生**空图片 block**（有 image 标签但无 file_id，页面显示空白），而不是跳过图片。图片只能通过三步流程上传：
  - `file_apply_upload` → Python `urllib.request.PUT` 上传到 COS → `file_commit_upload` → `block_create_block_descendant(image.session_id)`
  - ⚠️ COS 上传**必须用 Python `urllib.request`**，curl 会因 URL 特殊字符（%2F/%3B 等）返回 403
- 🚨 **`block_create_block_descendant` 的 index 参数**不等于 `block_list_block_children` 返回的直接子节点位置。API 使用包含嵌套子节点（quote/callout/toggle 等容器块的 children）的**扁平索引系统**。经验值：靠近页面顶部 offset 约 +1-2，页面中后部（Section 2-3）offset 约 +4-5。估算公式：直接子节点位置 + 前面所有嵌套子节点数量。**根本解法：优先用 `md_to_page.py` 或 MCP Direct HTTP Call 自动处理图片位置，避免手动计算 index**
- 🚨 **`after=""`** 是排末尾不是置顶，禁止使用
- 🚨 **LEXIANG_TOKEN 有效期约 2 小时**，每次用 `md_to_page.py` 前先从配置读取最新 token；token 失效或不可获取时，**自动切换到 MCP Direct HTTP Call 方法**（使用 WorkBuddy connector token，无需 LEXIANG_TOKEN），不要停下来问用户确认
- 🚨 **MCP Direct HTTP Call 的参数类型约束**：`file_apply_upload` 的 size、`block_create_block_descendant` 的 index 必须是字符串（如 `"12345"`、`"13"`），传整数会被 API 拒绝；MCP JSON-RPC 响应需要二次解析（`result['result']['content'][0]['text']` 是 JSON 字符串）
- 🚨 **全自动执行**：当首选方法不可用时，Agent 必须自动切换到降级方案完成全部操作（包括图片上传），**禁止输出任何需要用户确认才能继续的提示**（核心规则 #7）。只有在所有方法都失败时才报告错误

## Step 4：交付自检（🚨 每次任务结尾必做，不可跳过）

上传完成后，**必须**逐项检查以下清单，在回复用户时附上检查结果：

```
✅ 交付自检清单：
□ 1. 标题正确：文档标题与原文标题一致
□ 1b. 【播客/视频】Show Notes 完整：`## 节目介绍`/`## 视频介绍` 在 `## 逐字稿` 之前，含摘要与章节时间线（如有）
□ 2. 原文链接：文档中包含可追溯的原始 URL
□ 3. 图片完整：原文有 N 张图 → 乐享文档中有 N 张图（用 block_list_block_children 验证 image block 存在且有 file_id）
□ 3b. 【PDF】归档侧对账：本地 md 的 `![` 引用数 == 线上 image block 数（与 pdf-rich-translate 的「PDF 图表数 == 本地 ![ 数」凑成三方对账）
□ 4. 图片位置：用 block_fetch_page(render_mode="clean") 检查每张图片是否在正确的段落之间（不是聚集在页面底部或嵌套在引用块内）；每个图注块后须紧跟一张图
□ 4b. 【PDF】标注已渲染成专有块：`> [!stat]`/`> [!definition]` → callout 块；样式化表 → 原图 + 原生表格块（见 pdf-processing.md Step 3）
□ 4d. 【元规则·同类排查】若用户就同一类问题开口 ≥2 次（哪怕实例不同）→ 不许只修被指那一个；必须把问题抽象成特征、全文扫描所有同类实例、一次性全修，并在本轮自动更新 skill（L020）
□ 5. 翻译完整：非中文文章已翻译为中英对照，无遗漏段落
□ 6. 格式规范：标题层级、列表、引用等格式保留
□ 7. 目录正确：文档在正确的日期目录/指定目录下
□ 8. 链接可访问：返回的乐享链接格式正确
```

**图片验证方法**（第3-4项详细步骤）：
1. `block_list_block_children(entry_id=<文档ID>, with_descendants=True)` 获取所有 block
2. 筛选 `block_type == "image"` 的 block，检查是否有 `file_id`（有 = 上传成功，无 = 空占位符）
3. `block_fetch_page(entry_id=<文档ID>, render_mode="clean")` 获取渲染输出
4. 对照原文图片位置，逐张验证图片是否出现在正确的段落之间
5. 如果发现图片错位 → 删除错位 block → 用 `file_id` 在正确位置重新创建（无需重新上传）
6. 如果发现空图片 block → 立即补传图片，不要等用户发现

## Step 5：自省与学习

**触发条件**（满足任一即执行）：
1. 用户指出了本次执行中的错误或遗漏
2. 自检清单中有未通过的项
3. 执行过程中发现了新的技巧或踩坑经验
4. 【强制·自动】用户就**同一类**问题开口 ≥2 次（哪怕是不同实例）→ 立即判定为系统性问题，**不等用户说"更新 skill"**，本轮即：①全文同类排查并全部修复 ②沉淀根因到 lessons-learned ③更新自检清单+升版本号（L020）

**执行动作**：
- 读取 [references/lessons-learned.md](references/lessons-learned.md)
- 将新的教训追加到对应的严重性分级中
- 如果是 P0 级别的新教训 → 同时更新 SKILL.md 的核心规则或自检清单
- 更新规则演化记录表

## 参考文档（按需加载）

| 文件 | 何时加载 |
|------|----------|
| [references/lexiang-upload.md](references/lexiang-upload.md) | 上传到乐享时遇到问题、需要降级方案 |
| [references/pdf-processing.md](references/pdf-processing.md) | **PDF 归档侧**：把 pdf-rich-translate 产出的双语包导入乐享、标注渲染成专有块、增量改块（提取/翻译用 `pdf-rich-translate` skill） |
| [references/youtube-video.md](references/youtube-video.md) | 处理 YouTube 视频（下载+转录+翻译） |
| [references/podcast-audio.md](references/podcast-audio.md) | 处理播客音频（下载+转录） |
| [references/platform-specific.md](references/platform-specific.md) | 微信公众号/得到/SPA/微博等特定平台 |
| [references/tips-experience.md](references/tips-experience.md) | 经验总结、平台适配思路 |
| [references/troubleshooting.md](references/troubleshooting.md) | 常见问题排查 |
| [references/lessons-learned.md](references/lessons-learned.md) | 🔴 **每次执行前必读**：自省日志，历史教训和规则演化 |
