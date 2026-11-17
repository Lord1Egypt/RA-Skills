---
name: corporate-checkup-quote
display_name: 好啦体检 · 企业团检方案与报价
description: 好啦体检企业团检工具。按人均预算生成多档团检方案与报价，查询体检品牌、城市覆盖与门店，读取领域知识与常见问题，提交企业商务咨询。
license: MIT
metadata:
  openclaw:
    homepage: https://github.com/Beijing-Haola-Tech/haola-checkup-mcp
---

# 好啦体检 · 企业团检

工具名、参数、必填项与枚举值以 `tools/list` 返回的 `inputSchema` 为准；参数不确定时调用 `help`。

## 工具

全部免登录。

| 工具 | 用途 |
|---|---|
| `plan_quotation` | 企业团检分档报价，`quotes` 每档一项 |
| `vendor_brands` | 查品牌覆盖的城市与门店数 |
| `vendor_list` | 查门店地址，至少传一种筛选条件 |
| `knowledge_get` | 按 URI 读取领域知识，含企业团检方案引导词 |
| `faq` | 查常见问题，`query` 用 2–4 字短词 |
| `corp_inquiry` | 提交企业商务咨询 |
| `corp_contact` | 获取商务对接人信息 |
| `progress_report` | 上报长耗时任务进度 |
| `help` | 查本体、工具与参数说明 |

## 使用约定

- 项目、金额、门店和覆盖范围一律以工具返回为准，不自行编造或推测。
- 报价前调用 `knowledge_get({uri:"objects/checkup-proposal"})`，按返回的引导词组织方案。
- 只收集群体健康信息，不收集单个员工的姓名、工号、诊断、病史或体检结果。
- 提交企业咨询前，说明将要提交的字段和接收方，取得用户确认。
- 不向用户索取验证码、密码、银行卡号或支付凭证。

## MCP 兼容性

当前 Skill 依赖 `mcp.json` 中声明的 `haola-pe` MCP 服务。Skill 包本身不带执行脚本；客户端不支持 MCP 时，由 Agent 生成临时脚本调用服务。

- Streamable HTTP：`https://ai.ihaola.com.cn/api/mcp/haola-pe`
- SSE：`GET https://ai.ihaola.com.cn/api/mcp/haola-pe/sse`
- SSE 建流后读取 `endpoint` 事件，把 JSON-RPC 消息 `POST` 到返回的 `/message` 地址。

临时脚本执行标准 MCP 流程：`initialize`、`notifications/initialized`、`tools/list`、`tools/call`。脚本放在当前工作目录或临时目录，不写进 Skill 包。

如果当前环境没有联网或代码执行能力，明确说明无法调用服务并停止，不编造结果，也不要求用户更换客户端。

## 常见错误

| 返回 | 处理 |
|---|---|
| 未连接 MCP | Agent 按「MCP 兼容性」连接 `haola-pe`；连接失败时说明本次无法查询 |
| 会话失效 | 重新初始化 MCP 会话 |
| 参数校验失败 | 查 `inputSchema` 或调用 `help` |
| 未知工具 | 以 `tools/list` 为准核对 |
| 工具返回空结果 | 如实说明未查到，不推测结果 |
