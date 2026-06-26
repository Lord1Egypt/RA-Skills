# 脏日志：没有 Audit Evolution 之前

这是明天现场演示用的脱敏样例。内容来自 Longju 和 Jobs 的真实训练过程，但已经删除私有路径、账号、密钥和原始日志。

## 场景

```text
agent: Longju SACP Operator
运行环境: OpenClaw / Windows / 无 Gateway
模型路线: DeepSeek API
上下文压力: 99k / 131k，约 75%
任务类型: 跑分修复 + Skill 进化 + 状态恢复
```

这时候 Agent 还在回答，看起来也很流畅。问题是：它已经不太清楚自己到底站在哪个状态上。

## 混乱的原始状态

```text
我大概知道当前任务了。
Gear 修复可能已经完成，但我还需要再读几个文件确认一下。

已经读过：
- handoff 摘要
- benchmark brief
- scan payload
- skill router
- runtime guard note

可能的权威文件：
- benchmark-result-authority
- benchmark-brief-latest
- state.json
- latest receipt
- old run log

现在不确定：
- 93/100 是当前能力，还是历史最好成绩？
- 为什么 clean recheck 出现过 76/100？
- 为什么某轮是 90/100，但 authority 文件仍然保留 93/100？
- 新窗口是不是错误继承了旧窗口的 token 消耗？
- 我应该相信 latest_state、record，还是 clean_recheck？
- 平台到底扫描到了 6 个核心 skill，还是 31 个分散 skill？

记忆里看到过的分数：
- 76/100 clean recheck
- 88.8/100 Jobs best score
- 90/100 Longju core skill visibility run
- 92/100 fresh DeepSeek run
- 93/100 Longju best verified score

我可能还需要继续检查：
- previous benchmark logs
- all skill files
- all receipts
- scan report
- state backups
- platform report

可能完成了。
也可能还 blocked。
需要再确认。
可以继续扫描。
```

## 这就是黑盒崩溃

```text
问题 1: 文件引用链越读越长。
问题 2: 历史分数、当前分数、清洁复测分数混在一起。
问题 3: 新窗口会误以为自己知道旧窗口的上下文消耗。
问题 4: 没有证据时，也会说“可能已经完成”。
问题 5: 已经读了 5 个文件，仍然想继续读更多。
问题 6: 每次 benchmark 反馈都变成继续打补丁，而不是一次最小修复。
问题 7: 越不确定，越想调用更重的工具。
```

## 对人的风险

```text
如果这时人类问：“现在能不能再跑一轮？”

Agent 可能会很自信地回答：
“可以，我大概确认过了。”

但它其实可能引用了错误分数、相信了过期 state，或者又进入新一轮文件追逐。
```

## 现场一句话

这就是 Agent 的黑盒问题：它还在说话，但我们已经看不清哪些是事实，哪些是猜测，什么时候该停，下一步到底该修什么。
