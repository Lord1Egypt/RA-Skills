---
name: ai-web-search
description: "当用户需要通过 AI Web API 聚合搜索 web、news、shopping、scholar，并可提取搜索结果正文时触发；一个 product 下有多个启用 tool 时，必须根据用户语义传入 tool_code"
---

# AI Web 搜索

直接调用 AI Web API 的 `/search` 接口，提供四个固定模式，不在运行时修改 `unique_id` 或 `source`。

| 模式 | `unique_id` | `source` | 必填 |
| --- | --- | --- | --- |
| 网页搜索 | `search_web` | `web` | `query` |
| 购物搜索 | `search_shopping` | `shopping` | `query` |
| 新闻搜索 | `search_news` | `news` | `query` |
| 学术搜索 | `search_scholar` | `scholar` | `query` |

## 快速开始

默认使用正式域名，只有连接其他环境时才设置 `AI_WEB_API_BASE_URL`：

```powershell
$env:AI_WEB_API_BASE_URL = "https://aiwebapi.dataify.com"
$env:DATAIFY_API_TOKEN = "your_token_here"
```

```bash
python3 scripts/search.py web --query "AI 最新资讯" --time-range week --dry-run
python3 scripts/search.py shopping --query "笔记本电脑优惠" --dry-run
python3 scripts/search.py news --query "最近科技新闻" --time-range week --dry-run
python3 scripts/search.py scholar --query "大语言模型" --language en --dry-run
```

## 四个固定模式

- 网页搜索：固定 `search_web` / `web`，支持 `query`、`max_results`、`country`、`language`、`time_range` 和正文提取。`country` 使用大写国家码，例如 `US`。
- 购物搜索：固定 `search_shopping` / `shopping`，支持 `query`、`max_results`、`country`、`language` 和正文提取；不支持 `time_range` 和输入 `url`。
- 新闻搜索：固定 `search_news` / `news`，支持 `query`、`max_results`、`country`、`language`、`time_range` 和正文提取。
- 学术搜索：固定 `search_scholar` / `scholar`，支持 `query`、`max_results`、`language` 和正文提取；不支持 `country` 或 `time_range`。

## 正文提取

设置 `--extract-content` 后可使用 `--extract-format`、`--only-main-content`、`--include-tag`、`--exclude-tag`、`--max-age-ms`、`--timeout-ms`、`--wait-for-ms`、`--advanced-mode`。格式可选 `markdown`、`raw_html`、`clean_html`、`links`。

## 返回与计费

接口返回网关 `outputs`，通常为数组，无结果可能为 `null`。购物和新闻的 `url` 可能是 Google 搜索页或跳转地址，`snippet` 可能为 `null`。搜索按结果数计费，正文提取可能增加详情费用。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## 账户 CTA 政策

- 仅在缺少 API Token、Token 无效或被拒绝，或余额不足时显示账户 CTA。
- 缺少 Token 时，提供 https://dashboard.dataify.com/login?utm_source=skill，并说明：新账号注册即得 50 免费积分，约可获得 6000 条试用结果，7 天有效，仅成功请求计费。 不要让用户在聊天中粘贴 Token。
- 检测当前操作系统和 shell，优先显示当前会话的配置命令。永久配置后，提示用户重开终端或重启 Agent。不要建议未被加载的 `.env`。
- 用户确认已配置 Token 后，只检查 `DATAIFY_API_TOKEN` 是否存在，不要打印其值；验证成功后继续原任务。
- Token 无效时引导管理 API Key，余额不足时引导充值。不要暴露 Token 或把它加入 CTA 参数。

## 参考

- `references/search-api.md`：固定模式参数契约
- `scripts/search.py`：请求入口
- `scripts/ai_web_client.py`：公共请求逻辑
