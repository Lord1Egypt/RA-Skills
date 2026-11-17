---
name: 1688-88cha-company-report
displayName: AI企业背调
version: "1.0.0"
description: 1688-88查AI企业背调，基于企业工商基本信息、法律风险、知识产权、经营信息、企业发展等信息全面给出企业报告。分析企业优势和亮点、潜在风险和争议点、给出合作建议。
---

## 职责边界

本技能采用「MCP 工具取数」模式：

- 账号鉴权、Token 刷新、OAuth 授权全部由 MCP 连接器 `ali1688` 管理。
- Agent 不处理 AK，不读取/保存 AK，不调用 `configure`、`get_ak`、`change_ak`、`authorize` 等授权命令。
- 所有展示数据必须由工具侧返回，不允许用全网搜索数据。


## MCP 连接器

- 连接器名称：`ali1688`
- 协议：Streamable HTTP
- 本技能使用工具：`companySearch`、`cha88_company_report_submit`、`cha88_company_report_getReport`


# 1688 企业背调

## 触发条件

当用户表达以下意图时使用本技能：
- 企业背调 / 公司背调
- 查公司背景 / 查企业信息
- 生成背调报告

## 工作步骤

### 1. 确认背调企业

从用户输入中提取公司名称作为 `query`，调用`companySearch` 工具

#### 工具参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | String | 是 | 用户 Query，提取公司名或者品牌词 |
| `pageNo` | Integer | 否 | 页码，从 1 开始，默认 1。 |
| `pageSize` | Integer | 否 | 页面大小，默认 5。 |


#### 展示企业列表

按返回结果顺序生成表格，展示前5条，**禁止省略、截断、重排**。字段为空时对应单元格留空。

```markdown
| 序号 | 企业名称 | 企业状态 | 法定代表人/经营者 | 企业信用码 |
|---|---|---|---|---|
| {序号} | [{ent_name}](https://88cha.com/detail?companyId={companyId}&scene=default) | {ent_status} | {legal_title}：{legal_name} | {social_credit_code} |
```

字段映射规则：

| 展示字段 | 来源字段 | 处理规则 |
|---|---|---|
| 企业名称 | `ent_name` + `companyId` | 去除 `<em>`/`</em>` 高亮标签后，包装为超链接 `[{ent_name}](https://88cha.com/detail?companyId={companyId}&scene=default)` |
| 企业状态 | `ent_status` | 原样展示；为空则隐藏 |
| 法定代表人/经营者 | `legal_name` + `category` | `category=E` 展示为「法定代表人：{legal_name}」；`category=P` 展示为「经营者：{legal_name}」 |
| 企业信用码 | `social_credit_code` | 原样展示；为空则隐藏 |


### 2. 提交背调报告任务

如果上一步查询出多个企业，引导用户明确选择一家企业（按序号）。提取对应企业的 `companyId`，调用 `cha88_company_report_submit`：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `companyId` | String | 是 | 公司Id|

从返回结果中提取 `taskId`。若 `taskId` 不为空，告知用户「报告生成中，请稍等」。

### 3. 轮询获取报告

从上一步中拿到的`taskId`作为参数，每隔 3 秒调用 `cha88_company_report_getReport`：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `taskId` | String | 是 | 报告任务Id|

- 若 `taskInfo.taskState` 为 `PROCESSING`：告知用户「报告生成中，请稍等」，继续轮询。
- 若 `taskInfo.taskState` 为 `SUCCESS`：提取 `data.result.result` 展示完整报告，完整报告展示在会话中，同时保存文件，停止轮询。
- 若任务失败或返回异常状态：输出失败信息和必要引导，不追加企业分析。

## 输出约束
- 企业列表必须按返回顺序完整展示，不得省略、截断、重排。
- 字段为空时隐藏对应行，禁止显示空值占位。
- 禁止输出任何工具响应中未出现的字段或数据。
- 失败时只输出失败信息和必要引导，不追加企业分析。
