# Agent调用Skill异常上报 API 参考

> 上报 Agent 调用 Skill 异常，用于平台侧问题追踪与优化。异常上报不产生查询费用。
> 接口路径：`POST /agent/skill/error/report`
> 鉴权：需要 Bearer 令牌（UPKUAJING_API_KEY）

## python脚本参数

- `--params`：JSON格式的上报参数（必填）
- 未传 `skillId`/`skillVersion` 时，脚本会自动从当前 Skill 目录名与 SKILL.md 读取并填充
- 必填参数：`skillId`、`skillVersion`、`requestId`、`requestPath`、`context`；其中 `requestId` 从出问题的请求响应（ApiResp.requestId）中获取

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skillId | string | 是 | Skill 标识（最大128字符），如"customs-analysis-area" |
| skillVersion | string | 是 | Skill 版本（最大32字符） |
| agentName | string | 否 | Agent 名称（最大128字符） |
| modelName | string | 否 | 模型名称（最大128字符） |
| requestPath | string | 是 | 出问题的站内接口路径，以 / 开头（最大255字符），如"/agent/customs/analysis/area" |
| requestId | string | 是 | 全请求唯一关联号（最大128字符），取失败请求响应中的 requestId |
| requestTime | long | 否 | 请求发起时间戳（毫秒，≥0） |
| requestParams | object | 否 | 请求参数（原始入参，敏感字段会自动脱敏；序列化后≤64KB） |
| responseData | object | 否 | 响应数据（异常发生时的返回内容，敏感字段会自动脱敏；序列化后≤64KB） |
| durationMs | long | 否 | 本次调用耗时（毫秒，≥0） |
| context | string | 是 | 异常上下文（堆栈/错误信息，用于定位根因，最大2000字符） |

## 响应数据

### 外层结构

- code（integer）：状态码，0 表示成功
- msg（string）：提示信息
- requestId（string）：全请求唯一关联号（32位无横线，与 MDC traceId 同值）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| reportId | long | 上报记录 ID |
