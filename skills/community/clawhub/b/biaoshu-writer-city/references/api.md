# 百炼®标书开放 API 总调度

> **契约兼容标注（skill biaoshu-writer-city 3.1.2）**
> - 适配后端 API：`/api/open/v1`
> - 契约核对日期：2026-09-07
> - 本文件只做场景分发。执行具体任务时只读取对应分册，避免一次性加载全部接口细节。

## 先读哪个文件

| 当前任务 | 读取文件 |
|---|---|
| Api Key、鉴权、可用字数、限流、任务状态、结果下载、402 处理 | [api-auth.md](api-auth.md) |
| 智能解读、抽包、页数确认、生成成品标书、生成进度、成品短时下载链接 | [api-bid-workflow.md](api-bid-workflow.md) |
| 标书审查、暗标/电子标/敏感单位/语义审查、多文件合规报告 | [api-compliance.md](api-compliance.md) |
| 标书查重、2-3 份投标文件相似/雷同风险、可选招标文件基线 | [api-duplicate.md](api-duplicate.md) |
| 企业资料库查询、待填项本地回填字段解释 | [knowledge-fields.md](knowledge-fields.md) |

## 全局约定

- **Base URL**：`https://biaoshu.zhiliaobiaoxun.com/api/open/v1`
- **鉴权**：所有受保护接口都带 `X-App-Key: <Api Key>`。
- **任务模型**：提交接口返回 `job_id`；用 `GET /jobs/{job_id}` 轮询；用 `GET /jobs/{job_id}/result` 或 `download-url` 获取结果。
- **计费口径**：智能解读免费，可用字数为 0 也能发起；标书制作、标书审查、标书查重按平台规则消耗可用字数。标书生成的页数预估仅供参考，实际消耗以平台最终结算为准；生成前不做余额不足示警，也不做余额拦截。抽包、任务查询、结果获取、知识库查询等辅助查询不作为独立成果单独计费。
- **文件留存**：上传文件与任务结果以 Api Key 所属账户身份留存在百炼®标书服务器；任务结果与成品约 7 天后过期。
- **安全边界**：不要向用户展示或转发任何携带 Api Key / `bind_key` 的链接。

## 常见错误码

| HTTP | code | 处理 |
|---|---|---|
| 401 | `missing_credentials` / `invalid_credentials` | 检查或重置 Api Key |
| 402 | `insufficient_balance` / `insufficient_points` | 可用字数不足，提示购买会员或字数包后重试 |
| 404 | `not_found` / `job_not_found` / `project_not_found` / `result_expired` | 检查开放 API 开关、句柄归属或结果是否过期 |
| 409 | `invalid_job_state` / `report_task_conflict` | 等前置任务完成，或等待已有审查/查重任务结束 |
| 422 | `validation_error` | 检查文件数量、类型、大小、必填参数 |
| 413 | `bid_file_too_large` / `tender_file_too_large` / `batch_too_large` | 文件超限，压缩或拆分后重试 |
| 429 | `rate_limited` / `too_many_concurrent_jobs` | 退避重试或降低并发 |
| 500 | `internal_error` | 稍后重试或反馈平台 |
