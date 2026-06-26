---
name: freelancer-bidder
description: Scan Freelancer.com for new projects matching your skills, draft personalized bid proposals, and track bidding history. Use when you want to find freelance jobs, write winning bid proposals, or monitor new project postings on Freelancer.com.
---

# Freelancer Bidder

Automatically scan Freelancer.com for matching projects and draft personalized bid proposals.

## Capabilities

- Search active projects by keywords/skills
- Filter by budget, project type (fixed/hourly), and recency
- Draft personalized, professional bid proposals
- Track bid history and win rates
- Suggest optimal bid price based on project budget

## How to Use

Tell the agent:
- Your skills (e.g., "Python, data scraping, translation")
- Budget range preference
- Tone of proposals (professional / friendly / concise)

## Search Projects

```
Find Freelancer projects for: [your skills]
Budget: $[min]-$[max]
Posted within: last [N] hours
```

The agent will:
1. Fetch matching active projects via Freelancer API / web search
2. Rank by relevance and budget
3. Present top 5–10 opportunities

## Draft a Bid

```
Draft a bid for project: [project title / URL]
My background: [brief intro]
Tone: professional
```

The agent will generate a winning proposal including:
- Personalized opening (addresses client's specific need)
- Your relevant experience
- Clear delivery timeline
- Call to action

## Track History

Maintain a `bids.md` log in your workspace:
```
| Date | Project | Budget | Status |
|------|---------|--------|--------|
```

## Tips for Winning Bids

1. **Respond fast** — first 5 bidders get 60% more views
2. **Be specific** — reference the client's exact problem
3. **Keep it short** — under 150 words for fixed-price jobs
4. **Show, don't tell** — link to similar past work
5. **Ask one question** — shows genuine interest

## Workflow Example

```
User: Find Python scraping jobs under $200 posted today
Agent: [returns 8 matching projects with details]

User: Draft bid for project #3
Agent: [generates personalized 120-word proposal]

User: Submit and log it
Agent: [updates bids.md with entry]
```
