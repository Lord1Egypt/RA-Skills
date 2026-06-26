# Iteration-Aware Block Messaging

## Problem

Ralph 的 block 消息如果每次都一样（"Work is NOT done. Continue working."），agent 会进入 compliance mode——表面上继续工作，实际上反复生成"我已经完成了大部分工作"的变体直到被放行。固定消息在第 3 轮有效，到第 15 轮就被 agent 的内部推理"消化"掉了。

## Solution

Stop hook 的 block 消息根据当前迭代数动态变化。低迭代数用鼓励性消息，中段用对照检查消息，高迭代数用紧迫性消息。关键在于打破 agent 对固定模式的适应——每次消息的角度不同，迫使 agent 重新审视任务状态。

## Implementation

1. Stop hook 从 ralph.json 读取当前 iteration
2. 根据 iteration 范围选择消息模板
3. 消息中嵌入具体的行动指令而非笼统催促

```bash
ITERATION=$(jq -r '.iteration // 0' "$RALPH_FILE")

if [ "$ITERATION" -le 5 ]; then
  MSG="[RALPH ${ITERATION}] 任务进行中。检查你的任务清单，标记已完成项，继续处理下一项。"
elif [ "$ITERATION" -le 15 ]; then
  MSG="[RALPH ${ITERATION}] 不要声称'剩余工作可以后续完成'。
回到原始任务描述，逐条对照：哪些需求已满足？哪些还没动？
先列出未完成项，再继续。"
elif [ "$ITERATION" -le 30 ]; then
  MSG="[RALPH ${ITERATION}] 你已经工作了 ${ITERATION} 轮。
如果你觉得卡住了，换一个方法。
如果你在反复修同一个 bug，停下来重新阅读错误信息。
不要重复之前失败的操作。"
else
  MSG="[RALPH ${ITERATION}] 进入收尾模式。
优先完成核心需求，跳过 nice-to-have。
如果有未完成项无法在 5 轮内解决，写入 .working-state/remaining-work.md 作为 handoff。"
fi
```

4. 每个阶段的消息设计原则（基于 prompt-hardening P5 反推理阻断）：
   - **早期 (1-5)**：方向引导，不施压
   - **中期 (6-15)**：反合理化，要求具体对照
   - **后期 (16-30)**：反循环，鼓励换方法
   - **收尾 (30+)**：资源意识，优先级切换

## Tradeoffs

- **Pro**: 有效对抗 compliance mode 退化
- **Pro**: 后期消息引导 agent 做 graceful handoff 而非强行死磕
- **Con**: 阶段划分和消息内容需要根据经验调优
- **Con**: 消息长度增加了 context 消耗

## Source

OMC persistent-mode 的 Ralph block 消息观察。prompt-hardening P5（反推理阻断）原则——agent 在接收重复指令后会发展出"合理化绕过"策略。
