---
name: ai-startup-evaluator
description: "Evaluate whether an early-stage AI startup is worth joining as a technical contributor. This skill should be used when the user is considering joining a startup team, has received an offer or invitation from an AI startup, wants to assess a startup's health and prospects, or asks questions like 'should I join this startup', 'is this team worth joining', 'how to evaluate a startup offer', or 'red flags in AI startups'. Based on firsthand experience reflected in a detailed entrepreneurship review."
---

# AI Startup Evaluator

Evaluate whether an early-stage AI startup is worth joining. Provide a structured checklist
and red-flag detection, grounded in the lived experience of a full-stack engineer who spent
time in a pre-product/market-fit AI startup.

## When to Activate

Activate this skill when the user:
- Asks whether they should join a specific startup
- Describes a startup offer or team and wants evaluation
- Wants to know warning signs or green flags in AI startups
- Asks "is this normal" about startup practices

## Core Framework: 5-Resource Model

The essence of an AI startup is **"a game of converting knowledge into cash with extremely
limited resources."** Resources fall into five categories. Evaluate the startup across all five:

| Resource | What to Look For | Red Flags |
|----------|-----------------|-----------|
| **Talent (人才)** | Core team has complementary skills; not all juniors/interns; someone with management experience | CEO believes "every intern + Cursor = senior engineer"; 20 interns, 3 seniors; no one knows how to break down tasks |
| **Capital (启动资金)** | Clear runway (12+ months); realistic burn rate; matched to team size | "3 people can beat DeepSeek" mentality; spending on hype before product; unclear funding source |
| **Technology (技术)** | Tech stack matches domain; AI usage is deliberate; learning loops exist | Using AI as substitute for senior judgment; technical debt accumulating unchecked; chasing shiny tools |
| **Network (人脉)** | Founders have industry connections; distribution channels identified; access to early customers | Zero customer pipeline; founders isolated from market; "we'll figure out distribution later" |
| **Equipment (设备)** | Adequate hardware for the work (Macs for creative/ML work); cloud budget exists | Developers forced to use underpowered machines; no cloud support |

## Key Evaluation Dimensions

### 1. Team Composition

- What is the senior-to-junior ratio? A team of mostly interns with AI tools is a massive red flag
- Does anyone have management/project-management skills, or is everyone "just coding"?
- Are roles clearly defined, or is the CEO doing everything?
- Communication: does the team have overlapping schedules, or are people online at random hours?

### 2. Role Overload Detection

The most dangerous pattern: **one person wearing too many hats**.

Checklist:
- Is the CEO also CFO, CTO, PM, and HR?
- Do individual contributors also serve as project managers, DevOps, and QA — without recognition?
- Does anyone have an impossible workload that guarantees sleep deprivation?
- Is "async communication" actually a cover for "nobody knows when anyone is online"?

Result of role overload: sleep disruption → health decline → decision fatigue → burnout → attrition.

### 3. Progress Management Capability

Ask: **who breaks down work, who estimates, and who validates?**

Strong signal:
- Tasks are broken down by someone who understands BOTH the developer AND the requirement
- Estimation accounts for developer skill level (not all developers are equal)
- There is a feedback loop: was the estimate accurate? Did the developer learn?

Weak signal:
- CEO assigns work without understanding complexity
- No one tracks developer growth or skill regression
- Requirements are handed out as one-liner AI prompts

### 4. Technology & AI Usage Maturity

Good:
- AI is used to accelerate known patterns, not replace engineering judgment
- Code review catches AI-generated bugs (especially context-blind fixes)
- Team has a learning culture: knowledge is documented, not siloed

Bad:
- AI-written code pushed without review
- Bug fixes are one-off patches with no root-cause analysis
- CEO believes AI eliminates the need for senior engineers

### 5. Can You Learn from This Team?

The ultimate decision criterion: **"When I can no longer learn from the team, it's time to leave."**

Ask BEFORE joining:
- Who on this team can teach me something?
- Will I gain skills I can take elsewhere?
- Is the team's knowledge being documented and shared, or does it live only in people's heads?

## Decision Protocol

When evaluating, produce a structured output:

```
## Resource Scorecard (each /10)
- Talent: X/10 — [reason]
- Capital: X/10 — [reason]
- Technology: X/10 — [reason]
- Network: X/10 — [reason]
- Equipment: X/10 — [reason]

## Red Flags (list all)
## Green Flags (list all)
## Verdict: [Join / Conditional Join / Do Not Join]
## Key Risk: [single biggest concern]
```

## Additional Heuristics

- **The "3 people beat DeepSeek" test**: If the CEO thinks a tiny team can beat major players without extraordinary resources, walk away
- **The intern ratio test**: If >50% of technical staff are interns, the company is optimizing for cost over quality
- **The sleep test**: If anyone describes sacrificing sleep regularly to keep up, it's a structural problem, not a personal one
- **The school test**: Better schools → better alumni networks. If founders come from no-name backgrounds with zero network, distribution will be painful
- **The "what can I learn" test**: If you can't identify at least one specific skill you'll acquire, reconsider
- **The consolidation test**: Can the team's knowledge be converted into YOUR knowledge? If documentation and mentoring don't exist, you'll stagnate
