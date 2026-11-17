# Controller、阶段审查与独立 QA 2.1

派工、实现、阶段审查和最终验收的权限必须分开。

## Controller 派工

执行前，Controller 确认：

1. goal readiness 为 `Ready for Execution`；
2. 交付类别、规模与治理级别明确；
3. 范围、Non-Goals、写入边界和受保护边界一致；
4. 每条验收标准都有合适的证据；
5. 只授权一个阶段结果和一个 Next Action；
6. 已理解 `autonomy_mode: Bounded` 与 `acceptance_mode: Layered`。

只要持续产生有效进展、权限与方向未变化、没有触发停止条件，Developer 就可以跨已授权阶段自主继续。普通、可逆、项目内的技术选择不需要 Owner 批准。

## 阶段审查

用户在单 Agent `Controller -> Developer -> QC` 循环中的 `QC`，映射为 Stage Reviewer。

Stage Reviewer 只检查当前阶段：

- 验收标准与目标连接；
- 变更文件与范围；
- 聚焦命令结果与受影响回归；
- 行为声明所需的功能证据；
- 失败签名与返修进展；
- 重大风险与受保护边界。

阶段结论只能是 `Passed`、`Needs Fix` 或 `Blocked`。失败后在同一 Packet、同一 Work Order 返回 Developer，不创建新 Milestone。Standard/Full 的 Stage Reviewer 不能设置最终 QA 验收。

## 终端交接

所有 Standard/Full 授权阶段通过后，设置：

```text
execution_state: Ready for Independent Acceptance
stage_review: Passed
qa_decision: Not Reviewed
project_state: Active
```

独立 QA 必须由另一个 Agent、任务或人工审查者承担。它检查标准、diff、原始证据、限制、目标连接和必要目标环境，不能把 Developer 的期望结论当成证据。

## 独立 QA 决策

- `Accepted`：所有 Must Pass 标准和所需证据充分。
- `Accepted With Risk`：核心结果可用；非阻断风险明确、有负责人且有期限。
- `Failed`：仍有可执行的实现或证据缺陷。
- `Blocked`：验收需要当前无法取得的权限、环境、凭证或受保护访问。

核心流程损坏、缺少主要环境、没有功能证据，或仅 Contract 实现却声称 Runtime 时，不得使用 `Accepted With Risk`。

## 失败返修

阶段审查或 QA 失败时：

1. 保留同一 Milestone、Packet 与 Work Order；
2. 将返修绑定到失败标准 ID；
3. 在相应层设置 `Needs Fix`；
4. 重试前必须有新诊断或进展增量；
5. 重新运行聚焦验证与受影响回归；
6. 返修通过阶段审查后，才重新进入独立 QA。

## 风险连续携带规则

出现以下任一情况时，继续扩展前必须做 Direction Alignment：

- 同一重大风险连续两次出现在当前审查中；
- 连续三次独立决策为 `Accepted With Risk`。

复核必须判断该风险是否仍非阻断、是否需要目标或架构授权，或是否反映系统性测试不足。

## Lite 自验收

只有 Lite 且 `qa_required: false`、工作本地可逆、自动与功能证据通过、没有重大限制时，才可自验收。

`{baseDir}/templates/zh-CN/QA_DECISION.md` 只用于最终独立 QA，不用于日常阶段记录。
