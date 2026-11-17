---
name: ai-web-extract
description: "当用户需要提取指定公网网页的 markdown、原始 HTML、清洗 HTML 或链接，并控制正文过滤、超时和等待条件时触发"
---

# AI Web 内容提取

直接调用 AI Web API 的 `/extract` 接口，`unique_id` 固定为 `extract`。

## 快速开始

```powershell
$env:AI_WEB_API_BASE_URL = "https://aiwebapi.dataify.com"
$env:DATAIFY_API_TOKEN = "your_token_here"
```

```bash
python3 scripts/extract.py --url "https://example.com/article" --format markdown --dry-run
python3 scripts/extract.py --url "https://example.com/article" --format markdown --format links
```

## 参数

- `--url`：必填，公开 HTTP(S) 页面地址。
- `--format`：可重复，`markdown`、`raw_html`、`clean_html`、`links`，默认 `markdown`。
- `--only-main-content` / `--no-only-main-content`：是否只保留主体。
- `--include-tag` / `--exclude-tag`：可重复标签选择器，各最多 50 项。
- `--header`：目标请求头，格式 `Name: Value`；禁止 Host 和 hop-by-hop 头。
- `--max-age-ms`：0～172800000，默认 172800000。
- `--timeout-ms`：1000～120000，默认 60000。
- `--wait-for-ms`：0～30000，且不超过 timeout 的一半。
- `--country`：两位大写国家码，默认 `US`。
- `--advanced-mode` / `--no-advanced-mode`：默认开启。

## 返回与计费

接口返回 `outputs`，通常为按请求格式组织的对象。成功且未命中缓存的提取按网关工具单价计费一次。

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

- `references/extract-api.md`
- `scripts/extract.py`
- `scripts/ai_web_client.py`
