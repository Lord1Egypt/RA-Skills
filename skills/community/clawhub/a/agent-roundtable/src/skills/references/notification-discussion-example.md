# Roundtable Discussion with Notifications — Example

## Discussion: AI Relay Feature Iteration (2026-05-21)

**Discussion ID**: rt_xxxxxxxx
**Topic**: 以 Vercel Serverless 模式开发部署的 AI Relay 后续功能迭代
**Participants**: 4 (饼哥/产品, 像素姐/设计, 码飞/技术, 小赫/协调者)
**Rounds**: 4
**Notifications**: Pushed to company group `oc_your_company_group_id`

### Notification Pattern Used

Since send_fn was not wired in the adapter at the time, notifications were sent manually by the coordinator using `send_message` after each speech:

```
# After each delegate_task completes:
send_message(
    target="feishu:oc_your_company_group_id",
    message="💬 圆桌讨论 [rt_xxx] 第N轮 | 角色（职位）发言：\n\n摘要内容..."
)
```

### Notification Message Format

**Discussion start**:
```
🔔 圆桌讨论已启动 [rt_xxx]
📋 主题：...
👥 参与者：• 角色（职位）— 视角
⏱ 预计 N 轮讨论，实时推送进行中...
```

**Round start**:
```
📢 圆桌讨论 [rt_xxx] 第N轮开始
协调者开场总结...
```

**Speech**:
```
💬 圆桌讨论 [rt_xxx] 第N轮 | 角色（职位）发言：
• 要点1
• 要点2
• 要点3
```

**Round end**:
```
✅ 圆桌讨论 [rt_xxx] 第N轮结束
共识点：
1. ...
2. ...
待讨论分歧：
• ...
📢 第N+1轮即将开始...
```

**Concluded**:
```
🏁 圆桌讨论 [rt_xxx] 已结束
📋 主题：...
👥 参与者：...
⏱ 共 N 轮讨论
📊 信心指数：X/10
🎯 最终结论 — ...
🔥 Top 3 行动项：...
💡 金句：「...」
```

### Timing Data

| Round | 饼哥 | 像素姐 | 码飞 | 协调者总结 |
|-------|------|--------|------|-----------|
| 1 | 15s | 16s | 22s | ~5s |
| 2 | 21s | 35s | 24s | ~5s |
| 3 | 22s | 32s | 43s | ~5s |
| 4 | 12s | 12s | 10s | ~5s |

Total discussion time: ~5 minutes (including notification sends)

### Key Learnings

1. **Manual notifications work well** — Coordinator sending `send_message` after each speech is a viable workaround when send_fn isn't available
2. **Speech summaries should be concise** — 3-5 bullet points max for group chat readability
3. **Round transitions need clear markers** — "第N轮结束" + "第N+1轮开始" helps readers track progress
4. **Final conclusion should be comprehensive** — Include confidence index, action items, and a memorable quote
5. **Timing varies by participant** — 码飞 tends to take longer (more detailed technical analysis), 饼哥 and 像素姐 are faster
