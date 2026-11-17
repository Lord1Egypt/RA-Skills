# 执行合约 2.1

`Docs/ACTIVE_PACKET.md` 是治理与执行共同使用的精简当前授权。2.1 继续使用 `contract_version: "2.0"`，让现有读取器保持兼容。

## 新 Packet Frontmatter

```yaml
---
contract_version: "2.0"
packet_id: "GOAL-001"
goal_readiness: "Ready for Execution"
project_state: "Active"
execution_state: "Ready"
alignment_state: "Aligned"
stage_review: "Not Reviewed"
qa_required: true
qa_decision: "Not Reviewed"
size: "Medium"
governance: "Standard"
stage: 1
max_stages: 10
stage_minutes: 60
autonomy_mode: "Bounded"
acceptance_mode: "Layered"
delivery_class: "Runtime"
context_profile: "Compact"
write_scope: "."
outside_write_policy: "Deny"
authority_fingerprint: "sha256:..."
updated_at: "YYYY-MM-DDTHH:mm:ssZ"
---
```

旧 2.0 Packet 仍可读取。缺少 2.1 策略字段时采用保守默认值，并只产生一条迁移警告，而不是逐字段警告。

## 必要章节

- Desired Outcome
- User And Situation
- Current Stage Outcome
- Scope
- Non-Goals
- Acceptance Criteria
- Allowed Changes
- Protected Boundaries
- Evidence Required
- Stop Conditions
- Authority Sources
- Assumptions And Decisions
- Current Evidence
- One Next Action

新 Packet 原则上不超过约 120 行，并且只有一个立即行动。使用 `{baseDir}/templates/zh-CN/ACTIVE_PACKET.md`。

## 权限归属

| 字段或内容 | 权限 |
| --- | --- |
| Desired Outcome、Core Target、Non-Goals | Owner 或获授权 Controller |
| 规模、治理级别、交付类别、阶段、Work Order | Controller |
| 实现状态与执行证据 | Developer |
| 阶段审查 | Stage Reviewer |
| 方向对齐结论 | Controller 或指定对齐审查者 |
| 最终 QA 结论 | Standard/Full 的独立 QA |
| 项目验收状态 | Controller 在有效 QA 结论后更新 |

同一个 Agent 可以在有界执行中切换角色，但这不会产生独立验收权限。

## 分层状态流转

```text
Ready -> In Progress
In Progress -> Stage Reviewer Passed -> 下一授权阶段
In Progress -> Stage Reviewer Needs Fix -> Needs Fix -> In Progress
Standard/Full 终端阶段 -> Ready for Independent Acceptance
独立 QA Failed -> 同一 Packet、同一 Work Order 的 Needs Fix
独立 QA Accepted -> Accepted 或 Accepted With Risk
任何权限矛盾 -> Invalid State
```

旧 Packet 的 `Ready for Review` 继续兼容；新 Standard/Full 终端交付使用 `Ready for Independent Acceptance`。

## 权威指纹

只在 `Authority Sources` 列出当前权威文件。按列出顺序，以标准化项目相对路径和文件字节计算 SHA-256。指纹未变化时，不重复读取 TARGET、ACCEPTANCE 和 Work Order。

指纹变化必须先正式对齐。权威来源缺失或互相矛盾时，Bootstrap 保持只读，并输出一个合并后的 Owner 决策请求。

## 交付声明类别

- `Runtime`：已通过相应用户或操作流程验证的可执行行为。
- `Contract`：类型、接口、Schema 或兼容性规则。
- `Governance`：政策、流程、权限或状态控制材料。
- `Artifact`：文档、安装包、报告、fixture 或生成物。
- `Mixed`：跨多个类别；每条验收标准必须标注类别。

Contract、Governance 或 Artifact 通过，不等于 Runtime 功能可用。

## 写入规则

- 将工作区、Docs 目录、已有目标和新目标最近的已有父目录解析为真实路径。
- 拒绝任何通过 `..`、symlink 或 junction 越出工作区的写入。
- 尽可能原子更新 Packet。
- 一个当前事实只保留一个权威位置。
- 链接证据，不粘贴长日志。
- 向 `Docs/LOOP_RUNS.jsonl` 追加精简记录。
- 不保存凭证、私密数据、完整对话或隐藏推理。
