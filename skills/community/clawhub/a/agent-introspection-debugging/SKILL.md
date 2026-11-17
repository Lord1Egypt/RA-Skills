---
name: agent-introspection-debugging
description: "Debug agent behavior through four-stage self-diagnosis loop �� capture, diagnose, recover, report. Use when the agent needs structured self-debugging, error recovery, or behavioral analysis."
version: 1.0.0
origin: ECC (adapted for OpenClaw)
---

# Agent Introspection Debugging

Agent 自调试工作流。在盲目重试之前，先系统化地捕获、诊断、恢复和报告�?
## 触发条件

- 工具调用达到上限 / 循环限制
- 反复重试但无进展
- 上下文膨胀导致推理质量下降
- 文件系统/环境状态与预期不符
- 工具失败但可能通过诊断恢复

## 不用�?
- 代码变更后的功能验证 �?�?Backpressure 门控
- 框架特定调试 �?用语言专属 reviewer
- 运行�?Promise 问题 �?�?hook-engine

## 四阶段循�?
### Phase 1: Failure Capture（故障捕获）

在尝试恢复之前，精确记录失败状态�?
**捕获内容**�?- 错误类型、消息、堆栈（如有�?- 最后有意义的工具调用序�?- Agent 试图做什�?- 当前上下文压力：重复提示、过大日志、重复计�?- 当前环境假设：cwd、branch、服务状态、预期文�?
**最小捕获模�?*�?
```markdown
## Failure Capture
- Session / task: [会话/任务标识]
- Goal in progress: [当前目标]
- Error: [错误信息]
- Last successful step: [最后成功步骤]
- Last failed tool / command: [最后失败的工具/命令]
- Repeated pattern seen: [观察到的重复模式]
- Environment assumptions to verify: [需要验证的环境假设]
```

### Phase 2: Root-Cause Diagnosis（根因诊断）

在修改任何东西之前，先匹配已知模式�?
| 模式 | 可能原因 | 检查方�?|
|------|---------|---------|
| 最大工具调�?/ 重复相同命令 | 循环或无退出路�?| 检查最�?N 次工具调用是否重�?|
| 上下文溢�?/ 推理降级 | 无界笔记、重复计划、过大日�?| 检查近期上下文是否有重复和低信号内�?|
| 连接拒绝 / 超时 | 服务不可用或端口错误 | 验证服务健康、URL、端口假�?|
| 429 / 配额耗尽 | 重试风暴或缺少退�?| 计算重复调用次数和重试间�?|
| 写入后文件丢�?/ diff 过期 | 竞态、错�?cwd、分支漂�?| 重新检查路径、cwd、git status |
| 修复后测试仍失败 | 假设错误 | 隔离确切的失败测试，重新推导 bug |

**诊断问题**�?- 这是逻辑失败、状态失败、环境失败还是策略失败？
- Agent 是否失去了真实目标，开始优化错误的子任务？
- 失败是确定性的还是瞬态的�?- 什么是最小的可逆操作来验证诊断�?
### Phase 3: Contained Recovery（受控恢复）

用最小的操作改变诊断表面�?
**安全恢复操作**�?- 停止重复重试，重述假�?- 裁剪低信号上下文，只保留活动目标、阻塞点和证�?- 重新检查实际的文件系统/分支/进程状�?- 将任务缩小到一个失败命令、一个文件、一个测�?- 从推测性推理切换到直接观察
- 当失败是高风险或外部阻塞时，升级到人�?
**不要声称不支持的自动修复操作**，如"重置 Agent 状�?�?更新 harness 配置"，除非你真的通过当前环境中的真实工具在做这些�?
**受控恢复检查清�?*�?
```markdown
## Recovery Action
- Diagnosis chosen: [选择的诊断]
- Smallest action taken: [采取的最小操作]
- Why this is safe: [为什么这是安全的]
- What evidence would prove the fix worked: [什么证据能证明修复有效]
```

### Phase 4: Introspection Report（内省报告）

以报告结束，使恢复对下一�?Agent 或人类可读�?
```markdown
## Agent Self-Debug Report
- Session / task: [会话/任务]
- Failure: [失败描述]
- Root cause: [根因]
- Recovery action: [恢复操作]
- Result: success | partial | blocked
- Token / time burn risk: [token/时间消耗风险]
- Follow-up needed: [需要的后续]
- Preventive change to encode later: [后续要编码的预防措施]
```

## 恢复启发�?
按以下顺序优先选择干预措施�?
1. **用一句话重述真实目标**
2. **验证世界状态，而不是信任记�?*
3. **缩小失败范围**
4. **运行一个判别性检�?*
5. **然后才重�?*

**坏模�?*�?- 用稍微不同的措辞重试相同操作三次

**好模�?*�?- 捕获失败
- 分类模式
- 运行一个直接检�?- 只有当检查支持时才改变计�?
## 与现有系统的集成

| 场景 | 调用 |
|------|------|
| 恢复后代码变�?| �?Backpressure 门控验证 |
| 失败模式值得学习 | �?`.learnings/` 记录 |
| 问题不是技术失败而是决策模糊 | �?daily-agent 重新调度 |
| 失败来自冲突的本地状�?| �?workspace 审计 |

## 输出标准

当此技能激活时，不要只�?我修复了"结束�?
始终提供�?- 失败模式
- 根因假设
- 恢复操作
- 情况现在更好或仍然阻塞的证据
