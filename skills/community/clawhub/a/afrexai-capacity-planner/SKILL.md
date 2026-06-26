# Capacity Planner

Plan team and infrastructure capacity before it becomes a crisis.

## What It Does

Takes your current workload data — team size, utilization rates, project pipeline, seasonal patterns — and builds a forward-looking capacity model. Flags bottlenecks 4-8 weeks before they hit.

## When to Use

- Sprint planning feels like guesswork
- You're not sure if you can take on a new client/project
- Hiring decisions need data, not gut feel
- Infrastructure keeps getting slammed at predictable times

## How to Use

Tell the agent about your situation:

```
"We have 8 engineers, 3 active projects, and a new client starting in March. Can we handle it?"
```

The agent will:
1. **Audit current load** — Map people to commitments, calculate true utilization (not the number in your head)
2. **Model scenarios** — What happens if the new project lands? What if two people quit? What if scope grows 30%?
3. **Flag risks** — Identify single points of failure, overloaded roles, deadline clusters
4. **Recommend actions** — Hire, redistribute, defer, or say no — with numbers behind each option

## Capacity Framework

### Utilization Bands
| Band | Rate | Meaning |
|------|------|---------|
| 🟢 Green | <70% | Healthy buffer for unplanned work |
| 🟡 Yellow | 70-85% | Sustainable but tight |
| 🔴 Red | >85% | Burnout zone — something will slip |

### Key Metrics
- **Effective capacity** = headcount × available hours × efficiency factor (typically 0.7-0.8)
- **Demand pipeline** = committed hours + probable hours (weighted by likelihood)
- **Buffer ratio** = (capacity - demand) / capacity — target 15-25%
- **Time to constraint** = weeks until demand exceeds capacity at current trajectory

### Scenario Template
For each scenario, output:
- Headcount needed vs. available
- Skill gaps (specific roles/capabilities missing)
- Timeline risk (which deadlines move)
- Cost impact (overtime, contractors, lost revenue from saying no)
- Recommended action with confidence level

## Output Format

```
CAPACITY SNAPSHOT — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━
Team: [size] | Utilization: [%] | Buffer: [%]
Status: 🟢/🟡/🔴

CURRENT COMMITMENTS
- [Project A]: [X people, Y hours/week, end date]
- [Project B]: ...

PIPELINE (next 8 weeks)
- [Incoming work]: probability %, estimated load
- ...

RISKS
1. [Risk description + impact + timeframe]
2. ...

SCENARIOS
A) [Scenario]: [outcome summary]
B) [Scenario]: [outcome summary]

RECOMMENDATION
[Clear action with reasoning]
```

## Tips

- Refresh capacity snapshots weekly during planning
- Track actual vs. predicted utilization to calibrate your efficiency factor
- Include non-project work (meetings, support, admin) — it's usually 20-30% of capacity
- Don't plan above 80% utilization. The remaining 20% isn't slack, it's where real work happens.

## Go Deeper

Your capacity model is one piece of operational planning. For full business context packs covering finance, operations, and growth strategy across 10 industries:

→ **[AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)** — $47 each, built by operators who've done the work.

→ **[AI Revenue Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)** — Find out where your business is leaking money (free tool).

→ **[Agent Setup Wizard](https://afrexai-cto.github.io/agent-setup/)** — Get your AI agent configured for your specific business in 5 minutes.
