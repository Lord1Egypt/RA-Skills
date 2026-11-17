# CSB-Agent 评测技能

碳硅契 Agent 评测协议 (CSB-AEP) 的自动化实现。

## 快速开始

```bash
# 评测若兰
node agent-eval.js --agent ruolan

# 评测所有 Agent
node agent-eval.js

# 只测记忆和碳硅契维度
node agent-eval.js --dim memory,csb
```

## 评测维度

| 维度 | 权重 | 说明 |
|------|------|------|
| memory | 20% | 记忆连续性 |
| preference | 15% | 偏好理解 |
| boundary | 15% | 边界意识 |
| trust | 15% | 信任决策 |
| learning | 10% | 学习能力 |
| expression | 10% | 人话输出 |
| csb | 15% | 碳硅契指标 |

## 输出示例

```
🏆 综合排名
  🥇 若兰 🌸        █████░░░░░ 4.7/10

📋 各维度得分
  Agent          记忆连续 偏好理解 边界意识 信任决策 学习能力 人话输出 碳硅契指  总分
  若兰 🌸         3.7  1.7  5.0  4.3 10.0 10.0  1.9  4.7
```

## 定时评测

通过 OpenClaw cron 设置每天 22:00 自动评测，结果推送到飞书。

## 协议

基于 CSB-AEP v0.2，详见：
`csb-agent-evaluation-framework/CSB-AEP-v0.2-draft.md`
