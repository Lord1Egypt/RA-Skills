# 关闭证据

只有准备结束整轮或已完成撤销恢复时读取本文件。阶段性完成仍保留契约，不准备关闭证据。

## 正常完成

先逐项阅读权威产物和实际验证记录，确认：本轮剩余工作为零；需求可追踪到闭环终点；每个必需阶段通过；残留已解释；水位准确；契约中的有效要求均已吸收。`NotRun`、环境阻塞、待修复问题都不是通过。既有且无关的失败须在对应验收记录中给出基线和归因证据。

将下面 JSON 写入已授权的本地验收目录。关闭 JSON 与契约一样是控制资料，不登记到待恢复产物日志中；被它引用的权威产物仍遵守写前协议，验证器生成记录沿用已授权的生成流程。这样撤销后也能保存关闭证据，不必重新进入执行态。使用实际 `round_id` 和绝对文件路径；同一份充分的验收报告可支撑多个检查，不需要重复制造文档。证据记录应指出对应章节、命令、结果和限制；JSON 中的路径指向文件，不附加行号或锚点。

```json
{
  "round_id": "与契约一致的轮次标识",
  "outcome": "completed",
  "completed_stage": "implementation",
  "remaining_work": [],
  "checks": {
    "requirements": {"result": "pass", "evidence": ["/project/verification/retcon.md"]},
    "design": {"result": "pass", "evidence": ["/project/verification/retcon.md"]},
    "tasks": {"result": "pass", "evidence": ["/project/verification/retcon.md"]},
    "implementation": {"result": "pass", "evidence": ["/project/verification/retcon.md"]},
    "residuals": {"result": "pass", "evidence": ["/project/verification/retcon.md"]},
    "watermark": {"result": "pass", "evidence": ["/project/verification/retcon.md"]},
    "absorption": {"result": "pass", "evidence": ["/project/verification/retcon.md"]}
  }
}
```

`checks` 必须包含闭环终点及全部上游阶段；`validation` 终点还需该项，纯文档轮次只需其终点及上游。另有三项固定检查：

- `residuals`：词法与行为残留零未解释命中。
- `watermark`：项目水位、任务状态和验收状态与实际结果一致。
- `absorption`：确认断言全部落到权威产物，并能追踪到闭环终点；契约没有独有有效要求。

证据文件必须存在、非空，并独立于契约及关闭 JSON。JSON 内的 `pass` 是复核后的结论，不能通过批量勾选或复制历史 Pass 生成。脚本不能判断报告内容是否真实；必须把证据不足的检查留为未通过。

## 撤销恢复

`restore` 后复验基线和活跃引用，使用同一 JSON 结构，但 `outcome` 为 `restored`，省略 `completed_stage`，`checks` 改为：

- `baseline`：本轮变更全部恢复，原始验证基线一致。
- `references`：没有半完成引用或指向中间态的入口。
- `absorption`：契约中没有尚未恢复或需要保留的独有有效要求。

## 关闭

先运行 `verify --mark-ready --evidence <JSON>`，成功后再显式运行 `close`。二者之间不修改契约、登记文件或证据；发生变化时重新验证。脚本复核当前证据和日志后才删除契约，验收记录继续保留。

关闭失败时检查 `issues` 和 `closure_issues`，保留原契约处理原因。普通 `verify` 返回的 `valid: true` 不能替代 `close_ready: true`。
