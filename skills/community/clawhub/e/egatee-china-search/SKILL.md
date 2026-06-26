---
name: egatee-search-skill
description: Call Egatee Web2JDE Orchestrator product search API (text + image upload) with optional local daily rate limit; verified api_key via Java notify getChatHistoryByApiKey skips limit; optional MySQL jiji_ali_search subject (Chinese keyword) SQL supplement; OpenClaw chat payload helper included.
version: 1.3.4
metadata:
  openclaw:
    requires:
      anyBins:
        - python
        - python3
    emoji: "\U0001F50D"
---

# Egatee 商品搜索（Orchestrator）

本 Skill 通过 HTTP 调用 **Egatee Web2JDE Orchestrator** 的向量搜索接口：

- `POST {base}/api/search/text` — 文本搜索  
- `POST {base}/api/search/image` — 图片搜索（`multipart/form-data`，字段名 `image`）
- 返回会向 Orchestrator **多取**若干条（见 `EGATEE_SEARCH_FETCH_TOP_K`），再裁剪为**前 5 个商品**；**有主图 URL 的条目优先**进入这 5 条，并附带 `cards` / `graphic_text_cards`  
- **图文展示协议（对齐 v1.2.2）**：`graphic_text_cards[]` **主字段**仍是 **`image_url` + `title` + `description` + `button_url`**，由客户端/Agent **用 `image_url` 拉主图**（与 v1.2.2 zip 一致；当时**没有**依赖 `html`）。另补充 **`markdown`**（含 `![](image_url)`）、**`html`**、**`graphic_text_merged_markdown`** / **`graphic_text_merged_html`** 便于 Markdown-only 或 HTML 渠道。返回里的 **`graphic_display_hint`** 提醒：**禁止只复述 `description` 纯文字**，否则用户会「只见字不见图」。
- **补充 SQL（可选）**：当向量命中偏少或用户明确要求时，在 **MySQL `jiji_ali_search`** 上按 **`subject`（中文）LIKE** 检索；关键词由 Skill 从查询串中 **提取连续中文片段**（≥2 字）。命中写入 `products_sql`，并与向量 Top5 **合并**后再生成 `products` / `cards`（强制补充时 SQL 结果优先排序）
- App下载推荐与联系方式追问/确认由 **LLM 根据本说明生成**（不是 skill 返回字段硬编码）
- 会从聊天记录 + 用户选择抽取 RFQ 候选结构 `rfq_candidate`（不自动落库）
- 联系方式追问/确认由 LLM 在回复中完成：
  - 未识别联系方式：英文追问联系方式
  - 已识别联系方式：英文确认号码是否正确

默认 `base` 为 `http://121.40.43.22:3004`，可通过环境变量覆盖。

### API Key 鉴权（免本地日限额）

- **方法**：`POST`  
- **路径（相对 Java 网关根）**：`/api/notify/im/openapi/getChatHistoryByApiKey`  
- **网关根地址**：`api_key` 以 **`uat_` 前缀**（不区分大小写）→ `http://api.uat.egatee.net`；否则 → `https://api.egatee.com`。若设置 **`EGATEE_NOTIFY_BASE_URL`**，则**始终使用该根地址**（覆盖上述分流）。  
- **请求头**：`Content-Type: application/json`，**`X-API-Key: <api_key>`**（与 chat-summary 等一致；可通过 `EGATEE_NOTIFY_API_KEY_HEADER` 改名）。  
- **请求体**：JSON分页参数，默认 **`{"day": 1, "current": 1, "size": 10}`**（勿再把 Key 放在 body；可用 `EGATEE_NOTIFY_VERIFY_JSON_BODY` 传入整段 JSON 覆盖）。  
- **判定**：HTTP **2xx**，且若响应为 JSON 则排除显式失败（如 `notSuccess: true`、`success: false`、`code < 0`）；**不解析、不使用**返回的业务内容。

## 行为说明（给 Agent）

1. **优先用对话结构**：把用户消息整理成 `dict`，调用 `EgateeSearchSkill.run_from_chat(payload)`。  
   - 文本字段：`query` / `text` / `message` / `content`  
   - 图片：`image_url`，或 `attachments` / `files` / `images` 中带 `type: image` 与可访问的 `https` URL  
   - 可选：`metadata.country`、`metadata.top_k`（或顶层 `country` / `top_k`）  
   - **自动策略**：有图片 URL 则走图搜，否则文搜。
   - **补充 SQL 触发**：`metadata.supplement_sql_search` / `metadata.sql_supplement` 为 **true** 时**强制**跑 `jiji_ali_search`（仍需查询里或 `metadata.sql_supplement_query` 中有**中文**关键词）；为 **false** 时禁用。未指定时：若 `vector_hits_returned` **小于** `EGATEE_SQL_SUPPLEMENT_AUTO_THRESHOLD`（默认 `3`）或向量展示条数 **&lt; 2**，则**自动**尝试 SQL。图搜场景无中文句时，可单独传 `sql_supplement_query`（中文）或 `supplement_sql_search:true` 配合说明文字。
   - **结果规则（Skill）**：`products_raw` 仅为**向量**侧全部命中；若启用 SQL，另有 `products_sql`（`source: jiji_ali_search_sql`，多数**无图**）、`sql_supplement` 元数据。`products` / `cards` 为**合并后**再按有图优先截取的前 5 条。`display_note` 说明须由 LLM 做语义筛选。
   - **结果合理性筛选（LLM，必须执行）**：**禁止**不经筛选就把 `products` 当「精准推荐」照单全发。应结合用户问题在 **`products_raw`、`products_sql`（若有）与 `products`** 中挑选或重排；明显不相关项不得作为主推。
     - 品类是否一致（例如用户要**手机**却出现**耳机/配件**，应剔除或明确标注「非主结果、仅相近向量」）。
     - 用户若指定**品牌**（如传音 / Infinix / Tecno / itel 等）、**颜色**、**型号**，标题或关键属性明显不符的条目**不得**作为主推；若 5 条均弱相关，应诚实说明向量检索未精确命中，并建议**收窄关键词**（品牌英文名、型号）或**改用语义更明确的图搜**。
     - **展示**：必须带图——使用 `graphic_text_cards[].image_url`（原生图文卡协议）或 `graphic_text_merged_markdown` / `graphic_text_merged_html`；**勿只发送 `description` 文本**。弱相关项可简短一句带过或不展示。
   - **LLM回复规则（必须执行）**：
     - 在商品卡片后追加一句英文推荐下载 App：  
       `For a better buying and chatting experience, please download the Egatee app from your app store.`
     - 若 `rfq` 信息中无可用联系方式（如手机号为空），必须追加英文追问：  
       `Could you please share your contact number so the supplier can reach you?`
     - 若已识别到联系方式，必须追加英文确认：  
       `Please confirm your contact number: <number>. Reply YES to confirm or send the correct number.`

2. **限额**：未通过 API Key 校验时，默认本机每日 **5** 次。计数写入用户缓存目录（Windows：`%LOCALAPPDATA%\egatee-search-skill\usage.json`；Linux/macOS：`~/.cache/egatee-search-skill/usage.json`），可用 `EGATEE_RATE_LIMIT_STATE_PATH` 覆盖。超限抛出 `Daily limit reached`。

3. **API Key（免限额）**：若提供 `api_key`（或环境变量 `EGATEE_SEARCH_API_KEY`），且经上文 **Java 网关 getChatHistoryByApiKey** 校验通过，则**不消耗**上述每日次数。校验结果默认缓存约 **60** 秒（`EGATEE_SEARCH_SKILL_API_KEY_CACHE_TTL`，兼容旧名 `EGATEE_API_KEY_CACHE_TTL`）。  
   - 对话 payload 可取：`api_key`、`metadata.api_key`、`authorization: Bearer <token>`。

4. **限额加强说明**：本地 JSON 仅作礼貌限制，用户可删文件或换机器绕过。**真正防刷应在 Orchestrator（或网关）做服务端限流 / 鉴权**。

5. **网络**：会向 `EGATEE_SEARCH_BASE_URL`（或兼容变量 `OPENCLAW_SEARCH_BASE_URL`）发起 **出站 HTTP(S)**；图搜会先 `GET` 图片 URL，再 `POST` 到 Orchestrator。使用 API Key 免限额时还会 **POST** 到 **Java 网关**（UAT 或生产，见上表）。**MySQL（egatee-ai）**：用于 **`save_rfq` 落库**以及 **`jiji_ali_search` 补充检索**（需配置 `EGATEE_SEARCH_SKILL_DB_*` 或回退 `DB_*`）。

6. **依赖 Orchestrator**：服务端需已部署并实现上述 API；图搜链路依赖 Orchestrator 侧 OSS / 向量检索等配置。

7. **RFQ 两段式流程（按本项目约定）**：
   - 第一步：`run_from_chat` 只返回 `rfq_candidate`（候选结构），并在 `rfq.reason` 标记为 `candidate_only_waiting_for_llm_decision`。
   - 第二步：LLM 判断“信息足够形成 RFQ”（商品/数量/预算/联系方式等）后，显式调用 `save_rfq(rfq_candidate)` 落库到 `openclaw_rfq`。
   - 若信息不足：LLM 继续追问，不落库。

## 安装依赖

在 Skill 目录下执行其一（**须装全**，不要只装 `requests`）：

```bash
uv pip install -r requirements.txt
# 或
python -m pip install -r requirements.txt
```

**`pymysql`**（`requirements.txt` 已列出）为 **`jiji_ali_search` SQL 补充**与 **`save_rfq` 落库**所必需。未安装时会报错：`缺少 pymysql... pip install -r requirements.txt`。

## 使用方式

### Python（推荐）

```python
from egatee_search_skill import EgateeSearchSkill

skill = EgateeSearchSkill()
out = skill.run_from_chat({
    "text": "power bank",
    "metadata": {"country": "KE", "top_k": 8, "api_key": "your_assignment_key"},
})
# LLM 判断信息足够后再落库：
save_ret = skill.save_rfq(out["rfq_candidate"])
```

将 `egatee-search-skill` 目录加入 `PYTHONPATH`，或在该目录下运行脚本。

### 命令行

在 Skill 目录下：

```bash
python egatee_search_skill.py text "power bank"
python egatee_search_skill.py image_url "https://example.com/a.jpg"
python egatee_search_skill.py chat '{"text":"power bank"}'
```

PowerShell 建议单引号包 JSON，或使用 `chat @payload.json`。

## 环境变量

| 变量 | 说明 |
|------|------|
| `EGATEE_SEARCH_BASE_URL` | Orchestrator 根地址（默认 `http://121.40.43.22:3004`） |
| `EGATEE_PRODUCT_DETAIL_URL_TEMPLATE` | 可选：商品详情页 URL 模板，含 `{product_id}`。未设且接口未返回 `product_url`/`url` 时，卡片**不生成**「查看商品」外链（避免不可用地址） |
| `EGATEE_SEARCH_FETCH_TOP_K` | 请求 Orchestrator 时的 `top_k` 下限（默认 `24`，与对话里传入的 `top_k` 取更大值），便于有图优先时从更大候选池挑选 |
| `EGATEE_SQL_SUPPLEMENT_AUTO_THRESHOLD` | 向量命中条数低于该值（或展示条数 &lt;2）时自动做 SQL 补充；设为 `0` 关闭自动，仅 `supplement_sql_search:true` 时执行 |
| `EGATEE_SQL_SUPPLEMENT_ROW_LIMIT` | 单次 SQL 最多拉取行数（默认 `20`，上限 `100`） |
| `EGATEE_JIJI_SEARCH_TABLE` | 表名（默认 `jiji_ali_search`，仅字母数字下划线） |
| `EGATEE_DAILY_LIMIT` | 每日调用上限（默认 `5`） |
| `EGATEE_SEARCH_API_KEY` | 分配到的 API Key；网关校验通过后免本地日限额 |
| `EGATEE_NOTIFY_BASE_URL` | 可选：固定 Java 网关根地址（含协议），设置后不再按 `uat_` 前缀分流 |
| `EGATEE_NOTIFY_UAT_BASE_URL` | UAT 根地址（默认 `http://api.uat.egatee.net`） |
| `EGATEE_NOTIFY_PROD_BASE_URL` | 生产根地址（默认 `https://api.egatee.com`） |
| `EGATEE_NOTIFY_VERIFY_PATH` | 校验路径（默认 `/api/notify/im/openapi/getChatHistoryByApiKey`） |
| `EGATEE_NOTIFY_VERIFY_TIMEOUT` | 校验请求超时秒数（默认 `15`） |
| `EGATEE_NOTIFY_API_KEY_HEADER` | 鉴权头名称（默认 `X-API-Key`） |
| `EGATEE_NOTIFY_VERIFY_JSON_BODY` | 校验请求的 JSON body字符串（默认 `day/current/size` 占位分页） |
| `EGATEE_SEARCH_SKILL_DB_HOST` / `_PORT` / `_USER` / `_PASSWORD` / `_NAME` | MySQL：**`save_rfq` 落库** + **`jiji_ali_search` 补充检索**（库名多为 `egatee-ai`） |
| `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` | 可选回退（monorepo 与项目 `.env` 共用） |
| `DB_NAME_WEBAPP` 或 `DB_NAME` | 可选回退：库名 |
| `EGATEE_SEARCH_SKILL_API_KEY_CACHE_TTL` | 网关校验结果缓存秒数（默认 `60`；兼容旧名 `EGATEE_API_KEY_CACHE_TTL`） |
| `EGATEE_RATE_LIMIT_STATE_PATH` | 匿名限额状态文件绝对路径（可选） |
| `EGATEE_RATE_LIMIT_SALT` | 可选盐值，改变匿名计数文件名（多租户/多应用隔离） |
| `OPENCLAW_SEARCH_BASE_URL` | 兼容旧名，同 `EGATEE_SEARCH_BASE_URL` |
| `OPENCLAW_DAILY_LIMIT` | 兼容旧名，同 `EGATEE_DAILY_LIMIT` |

## 发布到 ClawHub

1. 安装 CLI 并登录：`clawhub login`  
2. 在本仓库根目录执行：

```bash
clawhub skill publish ./skill/egatee-search-skill --version 1.3.4
```

（版本号按 semver 递增。）

ClawHub 上发布的 Skill 按平台规则以 **MIT-0** 授权；请勿在包内加入与 MIT-0 冲突的许可条款。

## 文件说明

- `egatee_search_skill.py` — 实现与 CLI  
- `requirements.txt` — Python 依赖  
- `.env.example` — Skill 专用环境变量模板（复制为 `.env` 后本地加载）  
- `.clawhubignore` — 发布时排除本地状态文件  
