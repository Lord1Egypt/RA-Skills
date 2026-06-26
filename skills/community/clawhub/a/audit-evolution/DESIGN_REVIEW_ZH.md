# Audit Evolution 反思博弈审查

## 结论

当前版本可以作为 SkillHunt 和现场 Demo 的主 skill。它的核心卖点不是“又一个 memory skill”，而是把一次 Agent 运行变成下一轮可执行进化输入：

```text
证据 -> 状态 -> 记忆 -> 补丁 -> 测试 -> 下一轮启动
```

## 正方观点：为什么它有竞争力

- 用户入口足够短：一句“开始调用 Audit Evolution”即可触发。
- 不依赖 Agent 已经崩溃；benchmark、用户纠错、超时、上下文压力、skill 修改后都能触发。
- 比普通 memory 更克制：只记 verified fact、user feedback、decision、skill patch、retrieval key、next-run bootstrap。
- 比普通审计更闭环：不是只指出问题，而是输出一个最小补丁提案和下一轮启动指令。
- 现场证据够强：Longju 93.0、Jobs 88.8，以及两者的分数提升路径可以支撑“越跑越强”的故事。

## 反方攻击：它最容易被质疑什么

1. “这不就是总结日志吗？”
   - 回应：不是。它必须区分事实/反馈/旧声明/推断/未知，并且给出最小补丁、晋升门槛和下一轮启动指令。

2. “这不就是 memory skill 吗？”
   - 回应：不是全量记忆。它只沉淀可复查、可过期、可检索、能触发下一轮行动的 Memory Ledger Entry。

3. “用户还是要懂很多字段。”
   - 回应：用户只需要短指令：进化 / 保存 / 暂停 / 跑分 / 详情。字段是给 Agent 执行和审计用的。

4. “会不会自动乱改系统？”
   - 回应：不会。默认先审计和提出候选，应用补丁、本地测试、官方跑分、发布上传都需要明确边界。

5. “如果 Agent 没崩溃怎么办？”
   - 回应：它不是崩溃修复器，而是飞行记录仪。完成一次任务、拿到一次反馈、改过一次 skill，都应该留下下一轮进化输入。

## 当前仍有的弱点

- 没有跨框架 hook 的可执行安装器；不同 Agent 需要把自动触发规则接到自己的 wrapper / guard / task-end hook。
- 没有真实数据库型长期记忆；这是刻意取舍，优先公开传播和低依赖。
- 官方平台是否完全识别 `agents/openai.yaml`、frontmatter 和示例，仍需要 SkillHunt 导入后观察。

## 最小补强方向

1. 保持 README 中文第一屏清晰，不再堆理论。
2. 现场 Demo 只演示一条脏日志变成 Memory Ledger + Patch Proposal。
3. 让 Jobs 安装后跑一次本地闭环测试：用户只说“开始”或“进化”，看它是否能自动找证据。
4. 如果后续做 v0.4，再增加一个 script wrapper，把 run record 和 Memory Ledger 写入标准路径。

## 发布判断

```text
verdict: publish_ready_with_light_risk
risk: automation wrapper still framework-specific
recommended_demo: dirty_log.md -> clean_snapshot.md -> Memory Ledger Entry -> short command "进化"
```
