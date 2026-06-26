---
name: article_link
description: 文章链接提取工具。提交付费媒体文章链接，自动匹配已有内容并返回英文全文，或排队提取。支持 Barron's、Bloomberg、Financial Times、Foreign Policy、Handelsblatt、MarketWatch、New York Times、Reuters、The Atlantic、The Economist、The New Yorker、Wall Street Journal、Washington Post、Wired 共 15 家媒体。需要 Import Token 鉴权，每日有次数限制。Article link extraction tool. Supports Barron's, Bloomberg, FT, Foreign Policy, Handelsblatt, MarketWatch, NYT, Reuters, The Atlantic, The Economist, The New Yorker, WSJ, Washington Post, Wired (15 outlets). Requires Import Token.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"]
      }
    }
  }
---

# 文章链接提取工具

## ⚠️ 使用规则（必须遵守）

1. **只通过 CLI 命令调用** — 运行 `python3 {baseDir}/scripts/article_link.py <command>`，不要自己写脚本，不要用 curl/requests 直接调 API
2. **先读 config.json** — 执行任何命令前，先读取 `{baseDir}/config.json` 检查 `import_token` 是否已配置
3. **注意每日次数限制** — 基础模式 50 次/天，深度解析 5 次/天，提交前可先用 `quota` 查看剩余次数
4. **深度解析必须确认** — 使用 `--deep` 时脚本会自动拦截并返回配额信息，必须将配额告知用户并获得明确确认后，才能加 `--yes` 执行

## 第一步：检查配置

每次使用前先读取 `{baseDir}/config.json`：

```json
{
    "api_base": "https://pick-read.vip/api",
    "import_token": "imp-xxx..."
}
```

- 如果 `import_token` 为空 → 告知用户：请到 pick-read.vip 账户页生成导入令牌并填入 config.json
- 如果 `import_token` 已填写 → 直接执行命令，无需再传 `--token` 参数

## 工作流 A：查看支持的媒体来源

```bash
python3 {baseDir}/scripts/article_link.py media
```

返回示例：
```json
{
  "type": "media_list",
  "total": 15,
  "media": [
    {"domain": "ft.com", "name": "Financial Times"},
    {"domain": "wsj.com", "name": "Wall Street Journal"},
    {"domain": "nytimes.com", "name": "New York Times"}
  ]
}
```

## 工作流 B：查看今日配额

```bash
python3 {baseDir}/scripts/article_link.py quota
```

返回示例：
```json
{
  "type": "quota",
  "basic_used": 3,
  "basic_limit": 50,
  "deep_used": 0,
  "deep_limit": 5
}
```

## 工作流 C：提交文章链接

```bash
python3 {baseDir}/scripts/article_link.py submit "https://www.wsj.com/articles/some-article"
```

返回示例（已匹配 — 直接返回英文全文，无需额外命令）：
```json
{
  "type": "submit_matched",
  "job_id": "abc123",
  "origin_url": "https://www.wsj.com/articles/some-article",
  "source_media": "Wall Street Journal",
  "mode": "basic",
  "status": "matched",
  "matched_article_id": "def456",
  "title": "Article Title in English",
  "content_html": "<p>Full article text in English...</p>",
  "original_publish_time": "2026-04-10T08:00:00",
  "next_action": "done — 将 title + content_html 英文全文展示给用户"
}
```

→ **`type=submit_matched` 表示已拿到全文，直接展示 `title` + `content_html` 给用户即可**

返回示例（未匹配，排队提取）：
```json
{
  "type": "submit_pending",
  "job_id": "abc123",
  "origin_url": "https://www.wsj.com/articles/some-article",
  "source_media": "Wall Street Journal",
  "mode": "basic",
  "status": "pending_extract",
  "next_action": "poll — 用 status \"abc123\" 轮询任务状态"
}
```

→ **按 `next_action` 指引操作，无需自行判断**

可选参数：
- `--deep` — 深度解析模式，跳过已有匹配，直接重新提取
- `--yes` — 确认执行深度解析（必须在用户确认后才能使用）

### 深度解析确认流程（强制）

当用户要求深度解析时，必须分两步执行：

**步骤 1: 触发确认提示**
```bash
python3 {baseDir}/scripts/article_link.py submit "https://..." --deep
```

返回示例：
```json
{
  "type": "deep_confirm_required",
  "message": "深度解析每日仅 5 次，今日已用 1 次，剩余 4 次。请确认后使用 --yes 执行。",
  "deep_used": 1,
  "deep_limit": 5,
  "deep_remaining": 4,
  "confirm_command": "submit \"https://...\" --deep --yes"
}
```

→ **将 message 展示给用户，询问是否确认执行**

**步骤 2: 用户确认后执行**
```bash
python3 {baseDir}/scripts/article_link.py submit "https://..." --deep --yes
```

⚠️ **禁止跳过步骤 1 直接使用 `--deep --yes`，必须先让用户看到配额并确认**

**status 字段含义：**
- `matched` — 已匹配，脚本已自动获取英文全文，直接展示
- `pending_extract` — 未匹配，已排队等待提取，按 `next_action` 轮询
- `processing` — 提取进行中，继续轮询
- `ready` — 提取完成，脚本已自动获取全文
- `failed` — 提取失败，告知用户

## 工作流 D：查询任务状态

提交后如果 `type=submit_pending`，按 `next_action` 轮询：

```bash
python3 {baseDir}/scripts/article_link.py status "abc123"
```

返回示例（提取完成 — 自动返回英文全文）：
```json
{
  "type": "job_ready",
  "job_id": "abc123",
  "status": "ready",
  "matched_article_id": "def456",
  "title": "Article Title in English",
  "content_html": "<p>Full article text...</p>",
  "next_action": "done — 将 title + content_html 英文全文展示给用户"
}
```

返回示例（仍在处理中）：
```json
{
  "type": "job_status",
  "job_id": "abc123",
  "status": "processing",
  "next_action": "poll — 等待几秒后再次查询 status \"abc123\""
}
```

→ **始终按 `next_action` 操作，`done` 表示已拿到全文，`poll` 表示继续等待**

## 工作流 E：查看近期任务

```bash
python3 {baseDir}/scripts/article_link.py jobs
```

可选参数：`--page 2`、`--page-size 10`

## 工作流 F：单独获取英文全文（备用）

> 注意：`submit` 和 `status` 命令已自动在匹配/完成时获取全文。此命令仅在已知 `article_id` 时作为独立工具使用。

如果已有 `matched_article_id`，可直接调用：

```bash
python3 {baseDir}/scripts/article_link.py article "matched_article_id"
```

返回示例：
```json
{
  "type": "article_content",
  "id": "def456",
  "source_media": "Financial Times",
  "title": "Article Title in English",
  "content_html": "<p>Full article text in English...</p>",
  "origin_url": "https://www.ft.com/content/xxx",
  "original_publish_time": "2026-04-10T08:00:00"
}
```

→ **将 `title` 和 `content_html` 中的英文全文展示给用户**（content_html 是 HTML 格式，需解析后呈现纯文本）

## 工作流 G：组合任务示例

### 基础模式（最常用）

用户说“帮我看看这篇 FT 文章讲了什么”：

```bash
# 只需一步: submit 自动匹配 + 获取英文全文
python3 {baseDir}/scripts/article_link.py submit "https://www.ft.com/content/xxx"
# → type=submit_matched 时，直接展示 title + content_html
# → type=submit_pending 时，按 next_action 轮询
python3 {baseDir}/scripts/article_link.py status "返回的job_id"
```

### 深度解析模式

用户说“帮我深度解析这篇 FT 文章”：

```bash
# 步骤 1: 触发确认
python3 {baseDir}/scripts/article_link.py submit "https://www.ft.com/content/xxx" --deep
# → 返回 deep_confirm_required，将 message 展示给用户

# 步骤 2: 用户确认“是”后才执行
python3 {baseDir}/scripts/article_link.py submit "https://www.ft.com/content/xxx" --deep --yes
# → 按 next_action 处理结果
```

### 核心原则：始终按 `next_action` 操作

- `next_action` 以 `done` 开头 → 直接展示 `title` + `content_html` 给用户
- `next_action` 以 `poll` 开头 → 等待几秒后执行其中的命令

## 支持的媒体来源

| 媒体 | 域名 |
|---|---|
| Barron's | barrons.com |
| Bloomberg | bloomberg.com |
| Financial Times | ft.com |
| Foreign Policy | foreignpolicy.com |
| Handelsblatt | handelsblatt.com |
| MarketWatch | marketwatch.com |
| New York Times | nytimes.com |
| Newsweek | newsweek.com |
| Reuters | reuters.com |
| The Atlantic | theatlantic.com |
| The Economist | economist.com |
| The New Yorker | newyorker.com |
| Wall Street Journal | wsj.com |
| Washington Post | washingtonpost.com |
| Wired | wired.com |

## 每日次数限制

| 模式 | 每人每天上限 | 说明 |
|---|---|---|
| 基础模式 (basic) | 50 次 | 先匹配已有内容，未命中则排队提取 |
| 深度解析 (deep) | 5 次 | 跳过匹配，直接重新提取 |

## 禁止事项

- ✘ 不要用 curl、wget、requests 等直接调用 API
- ✘ 不要自己拼 URL 或写 HTTP 请求代码
- ✘ 不要猜测 API 端点路径
- ✘ 不要编造文章内容或摘要
- ✘ 提取失败时不得编造内容，应如实告知用户

## 故障排查

| 现象 | 原因 | 解决 |
|---|---|---|
| `401: 缺少导入令牌` | config.json 中 import_token 为空 | 让用户到 pick-read.vip 生成令牌 |
| `401: 导入令牌无效或已被撤销` | token 错误或已重置 | 重新生成令牌 |
| `403: 订阅已过期` | 用户订阅到期 | 告知用户需要续订 |
| `422: 不支持该媒体来源` | 链接不在白名单中 | 用 `media` 命令查看支持列表 |
| `429: 今日已达上限` | 每日次数用尽 | 用 `quota` 查看配额，明天再试 |
| `EOF occurred in violation of protocol` | 系统代理干扰 TLS | 脚本已内置代理绕过，正常重试 |
