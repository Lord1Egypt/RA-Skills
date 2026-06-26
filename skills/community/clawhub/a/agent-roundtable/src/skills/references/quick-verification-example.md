# Quick Verification Discussion — Working Example

From session 2026-05-23: Boss requested a roundtable demo to verify the skill.
Topic: "明天吃什么" (What to eat tomorrow).

## Why This Pattern Works

When Boss says "组织一次会议看效果", the goal is to verify the full pipeline:
- Discussion creation with web=True and notifications
- Multi-round structured discussion
- WebViewer live display
- Feishu group chat notification sync
- Conclusion and convergence

The direct API pattern (coordinator drives all speeches) runs in ~2 minutes
vs ~15-20 minutes for full delegate_task delegation. Fast enough for demo,
reliable enough for verification.

## Setup

```python
core.create_discussion(
    topic="明天吃什么",
    context="团队午餐讨论，预算人均50-80元，公司在深圳南山区",
    participants=[
        {"profile": "bingge", "role": "产品总监", "perspective": "注重口味和体验", "display_name": "饼哥"},
        {"profile": "pixiel", "role": "设计师", "perspective": "注重食物颜值和环境", "display_name": "像素姐"},
        {"profile": "mafei", "role": "开发工程师", "perspective": "注重性价比和效率", "display_name": "码飞"},
    ],
    created_by="coordinator",
    max_rounds=3,
    web=True,
    web_port=8199,
    notifications={
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_your_company_group_id"}],
        "events": ["round_start", "speech", "round_end", "concluded"]
    }
)
```

## Execution Flow

1. **Init** → `create_discussion()` → get `discussion_id` + `web_url`
2. **Round 0** → coordinator opening statement via `core.speak()`
3. **Round 1-3** → coordinator speaks FOR each participant via `core.speak()`
   - Each round: coordinator summary, then bingge, pixiel, mafei
   - Notifications auto-fire on each speech (if send_fn wired)
4. **Conclude** → `core.end_discussion()` → concluded notification fires

## Results

- Total time: ~2 minutes
- 12 speeches across 3 rounds + opening
- WebViewer URL auto-generated (port auto-increments if busy)
- 12 Feishu notifications sent to company group
- Full discussion history persisted to roundtable.db

## Key Observation

The coordinator generates each participant's speech content based on their
role and perspective. This produces realistic, role-consistent content that
demonstrates the discussion format without the overhead of real sub-agents.

For production discussions where genuine independent analysis is needed,
use the full delegate_task pattern (but verify tool_trace is non-empty).
