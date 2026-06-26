# 安全与隐私说明

## 认证与凭证

本技能调用 Datu 外部 API，需要用户自行创建并控制一个 API Key。

- Required env vars: `DATU_API_KEY`
- Primary credential: `DATU_API_KEY`
- Request header: `X-API-Key`
- Host credential persistence: when a user provides a Datu API Key in Feishu, WeChat, OpenClaw, ClawHub, or another host, the host should save it as the `DATU_API_KEY` 持久凭据 and automatically inject it for later calls.
- The skill should not repeatedly ask the user for the same API Key. Ask the user to reconfigure it only when the persistent credential is missing, deleted, expired, or rejected by the Datu API.
- If `DATU_API_KEY` is unavailable after prior successful use, first check the host credential vault, secret storage, or skill authorization settings.
- 宿主收到用户提供的 Datu API Key 后，应保存为 `DATU_API_KEY` 持久凭据，并在后续调用中自动注入。
- 不要反复要求用户重新提供 API Key；只有持久凭据缺失、被删除、失效或认证失败时，才提示用户重新配置。

```bash
DATU_API_KEY=your_api_key_here
```

```http
X-API-Key: your_api_key_here
```

不要把 API Key 写入公开代码仓库、公开聊天记录或可共享文档。

## 外部接口

本技能会向以下外部服务发送请求：

- API base: `https://datu.digilifeform.com/api`
- Homepage: `https://datu.digilifeform.com`
- Privacy policy: `https://datu.digilifeform.com/privacy`

主要接口包括：

- `POST /api/datu/create`
- `POST /api/datu/create-from-file`
- `POST /api/datu/create-combined`
- `POST /api/edit/create`
- `GET /api/datu/status/{task_id}`
- `GET /api/edit/status/{task_id}`
- `GET /api/tasks/{task_id}/research-report-link`

## 会发送的数据类型

根据用户选择的功能，请求中可能包含：

- 用户输入文本
- 上传文件内容
- 原图 URL
- 标注图 URL
- 参考图 URL
- 任务状态查询信息

如果用户启用 `deep_research=true`，Datu 会进行全网深度抓取与分析，并返回 Word `.docx` 深度研究报告。

## 上传前安全检查

在提交文本、文件或图片 URL 之前，应先做一次轻量敏感信息检查。以下内容如果明显出现，不应默认上传，应先提醒用户并获得明确授权：

- API Key、密码、访问令牌、私钥、Cookie、数据库连接串
- 身份证号、护照号、银行卡号、医疗记录、精确住址等高敏个人信息
- 受监管、受保密协议、受合同限制或公司内部禁止外发的数据

如果用户不确认，应停止上传，或请用户提供脱敏版本。

## 保真提交的边界

本技能强调“保真提交”是为了避免外层代理先摘要、压缩或改写用户资料，导致生成结果丢失关键信息。这个规则只适用于上传前安全检查通过后的普通业务资料。

不要把风险控制理解为默认摘要。正确顺序是：

1. 检查是否存在明显敏感或受限内容。
2. 如存在风险，先提醒并等待用户明确授权或脱敏版本。
3. 如不存在明显风险，再保真提交用户资料，由 Datu 内部完成解析、研究、整理和生成。

## 深度研究确认

`deep_research=true` 只能在用户明确选择或确认后启用。它会：

- 向 Datu 外部服务发送用户提供的资料。
- 触发全网深度抓取与分析。
- 增加通常约 5-15 分钟处理时间。
- 额外消耗 5 积分。
- 生成可下载的 Word `.docx` 研究报告。

## 数据用途与保留

这些数据用于创建和处理大图生成、深度研究、AI 修图与任务状态查询。生成结果默认保留约 30 天，具体以官网隐私政策和服务端策略为准。

建议先用非敏感数据测试工作流；如需处理受限资料，请先确认自身合规要求。
