# Roundtable with Real-time Notifications — Working Example

From session 2026-05-21: 4-round discussion about AI Relay iteration planning
with real-time push to Feishu company group.

## Setup

Discussion created with notifications config:
```python
roundtable_init(
    topic="以 Vercel Serverless 模式开发部署的 AI Relay 后续功能迭代",
    participants=[
        {"profile": "bingge", "role": "产品总监", "perspective": "关注用户需求、产品定位、商业化", "display_name": "饼哥"},
        {"profile": "pixiel", "role": "设计总监", "perspective": "关注管理后台体验、数据可视化", "display_name": "像素姐"},
        {"profile": "mafei", "role": "技术总监", "perspective": "关注 Serverless 架构约束、技术可行性", "display_name": "码飞"},
        {"profile": "default", "role": "协调者", "perspective": "关注团队协作、优先级排序", "display_name": "小赫"},
    ],
    max_rounds=4,
    notifications={
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_your_company_group_id"}],
        "events": ["round_start", "speech", "round_end", "concluded"]
    }
)
```

## Coordinator Workflow (with manual notifications)

Since send_fn isn't wired in the adapter, the coordinator manually drives notifications:

### 1. Opening
```
# Send launch notification
send_message(target="feishu:oc_xxx", message="🔔 圆桌讨论已启动 [rt_xxx]\n📋 主题: ...\n👥 参与者: ...\n⏱ 预计 N 轮")

# Coordinator opening statement
roundtable_speak(discussion_id="rt_xxx", participant="coordinator", content="...")

# Send round_start notification
send_message(target="feishu:oc_xxx", message="📢 第1轮开始\n协调者开场: ...")
```

### 2. Each Round — Sequential Delegation
```
for participant in participants:
    # Delegate to participant
    delegate_task(
        goal="你是{角色}，请从{角度}发表观点，然后调用 roundtable_speak 记录发言。",
        context="... full discussion history + role context ...",
        toolsets=["roundtable"]
    )
    
    # Send speech notification (200-char summary)
    send_message(target="feishu:oc_xxx", message="💬 第N轮 | {角色}（{名字}）发言：\n{摘要}")
```

### 3. Round Summary
```
# Coordinator summarizes round
roundtable_speak(discussion_id="rt_xxx", participant="coordinator", content="Round N 小结: ...")

# Send round_end notification
send_message(target="feishu:oc_xxx", message="✅ 第N轮结束\n共识点: ...\n待讨论: ...")
```

### 4. Final Round + Conclusion
```
# Each participant gives final statement with confidence index
delegate_task(goal="... 最终总结陈词，给出信心指数 ...")

# End discussion
roundtable_end(discussion_id="rt_xxx", conclusion="...")

# Send concluded notification
send_message(target="feishu:oc_xxx", message="🏁 讨论结束\n📊 信心指数: N/10\n🎯 结论: ...")
```

## Timing Data
- Total duration: ~5 minutes for 4 rounds, 4 participants
- Each delegate_task call: 10-45 seconds
- Round 3-4 were faster (participants had accumulated context)
- Coordinator overhead: ~2-3 minutes for summaries + notifications

## Notification Message Format Reference

| Event | Format |
|-------|--------|
| Launch | 🔔 圆桌讨论已启动 [rt_xxx] + 主题 + 参与者 |
| Round start | 📢 第N轮开始 + 协调者开场摘要 |
| Speech | 💬 第N轮 \| 角色(名字) 发言: + 200字摘要 |
| Round end | ✅ 第N轮结束 + 共识点 + 待讨论分歧 |
| Concluded | 🏁 讨论结束 + 信心指数 + 结论 + Top行动项 |

## Lessons Learned
- Sequential delegation (not parallel) is critical — participants build on each other
- Round 3-4 are faster because accumulated context reduces token usage
- Manual notifications add ~2min overhead but give Boss full visibility
- 200-char speech summaries work well for Feishu group readability
- The coordinator's round summary is the most valuable signal — don't skip it
