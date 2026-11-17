# 对齐、重基线、审计与完成线 2.1

每次只使用一种权限模式。方向检查不能静默改写目标，审计也不能签署验收。

## 每阶段轻量对齐

每个阶段记录：

1. 用户或操作人员得到什么变化；
2. 它服务哪个目标与标准；
3. 范围、假设或架构是否移动；
4. 哪些证据可否定过早完成；
5. Next Action 是否仍是最高价值的已授权动作。

只在 Loop 里保留精简增量。

## 正式对齐

在阶段 3、6、10 后执行；以下情况立即执行：

- authority fingerprint 变化；
- 预计范围增长超过 20%；
- 自动检查全绿但主要用户流程失败；
- 无法用一句话说明目标连接；
- 同一失败签名连续两次没有新证据；
- 同一重大风险连续携带两次；
- 连续三次最终结论为 `Accepted With Risk`；
- 新想法影响目标、Non-Goals、受保护架构/数据、发布或生产行为。

可用结论：

- `Aligned - Continue`
- `Aligned - Ready for Independent Acceptance`
- `At Risk`
- `Locally Compliant, Globally Misaligned`
- `Owner Review Required`
- `Blocked`

正式对齐可以重新定级、拆分、暂停或请求 Owner 决策，但不能自行授权目标变化。

## 新想法分类

将新想法分为 `Observation`、`Clarification`、`Improvement Candidate`、`Scope Change`、`Core Target Change` 或 `Conflict`。只有不改变验收和 Non-Goals 的澄清，才可立即进入当前工作。

## 目标重基线

比较旧目标、新需求、用户价值、保留或失效的工作、验收变化、成本、风险及 Owner 决策。结论只能是：

- `No Target Change`
- `Clarification Only`
- `Scope Change Approved`
- `Core Target Change Approved`
- `Owner Decision Required`
- `Reject / Defer`

重基线过程不实现、不派工。批准后更新权威文件、重新生成指纹，再独立进行 Planning/Dispatch。

## 全项目审计

审计默认只读，可以使用更宽但明确的上下文预算。必须分开陈述已验证事实、缺失证据、风险债务、矛盾声明、缺乏全局价值的局部成功及 Owner 决策。Contract 一致性、Artifact 存在和 Runtime 可用性分别评分。

## 完成线

定义原始目标、当前用户可见能力、Must Finish、Not Required Now、应停止扩张的工作、下一个独立有价值交付及最终证据。只有完整能力获得所需验收后，Milestone 才关闭。
