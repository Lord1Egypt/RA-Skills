# Real-world before/after examples

These examples show what a cleanup pass looks like in practice.

The "before" versions are intentionally rough. The "after" versions keep the same meaning but sound like a person wrote them.

## Example 1: Product description

### Before (score: 45)

> Here is a quick overview of our platform. It plays a crucial role in modern operations and helps teams streamline work across many systems. The future looks bright as adoption continues to grow.

### After (score: 6)

> The platform connects Slack, Jira, and Salesforce in one setup flow that takes about 20 minutes.
>
> We shipped AI search in March. In a beta with 50 teams, users reported spending about 30% less time looking for files.
>
> Pricing starts at $15 per user/month, with a free tier for teams under five.

---

## Example 2: City description

### Before (score: 41)

> Portland is a vibrant city with a rich culture and a thriving food scene. It continues to grow despite challenges and remains a major destination in the region.

### After (score: 4)

> Portland has about 650,000 residents and sits on the Willamette River.
>
> The city has more than 500 licensed food carts, which is one reason visitors keep coming back.
>
> It rains around 155 days a year, so indoor spaces like cafés and bookstores matter more than in most US cities.

---

## Example 3: Team update email

### Before (score: 52)

> I hope this message finds you well. I wanted to take a moment to provide a comprehensive update on Q3 performance. It is important to note that our progress reflects strong alignment across teams. Let me know if you have any questions.

### After (score: 3)

> Hi team,
>
> Q3 revenue closed at $2.4M, up 12% from Q2. Most of that came from the Harris expansion in August.
>
> Two risks for Q4: pipeline coverage is thin, and we still need two sales hires. I want final candidates by mid-October.
>
> Full deck is attached. Let's review at Thursday's standup.

---

## Run these examples locally

```bash
# Compare a rough draft against a revised one
humanizer compare --before draft-before.md --after draft-after.md

# Scan all docs and fail CI if any file is above your threshold
humanizer scan docs --ext md --fail-above 45
```
