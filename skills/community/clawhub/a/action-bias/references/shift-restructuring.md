# Shift Restructuring Guide

How to convert report-producing agent shifts into action-producing ones.

## Before/After Examples

### Research Agent

**Before (report mode):**
```
RESEARCH SHIFT: Scan for new competitors. Check forums and social
media for market signals. Flag threats or opportunities. Write
report to memory/research-report.md.
```

**After (action mode):**
```
RESEARCH SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST produce at least 1 outbound action alongside your research.
Pure reports = failure.

## Research (keep doing this):
- Scan for new competitors
- Check forums, communities, social media for market signals
- Flag threats or opportunities

## Required Outbound (pick 1+):

1. **Find 3+ prospects** — Search community "what are you working on"
   threads, launch announcements, and forum posts. Extract: name,
   company, URL, contact info. Save to data/prospect-pipeline.md

2. **Post an insight** — Turn one research finding into a social
   media post. [exact tool/command to post]

3. **Draft a content angle** — If you find an interesting trend,
   write a 200-word blog outline and save to memory/content-ideas.md

## Log:
Append findings AND actions taken to memory/research-actions.md
```

**What changed:**
- Added "OUTBOUND ACTIONS REQUIRED" header
- Kept research (it's valuable) but made it serve an action
- Provided 3 specific action options with tools/commands
- Added logging requirement for both research AND actions

### Marketing Agent

**Before:**
```
MARKETING SHIFT: Review our channels. Propose content ideas.
Analyze what's working. Write a strategy update.
```

**After:**
```
MARKETING SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST complete at least 2 outbound actions. Reports alone = failure.

## Required Actions (pick 2+):

1. **Post on social media** — [exact tool/command]
   Write something genuinely useful. Not promotional.

2. **Submit to a directory or listing** — Check your log for
   what's done. Try new ones. Use browser or API.

3. **Write and publish a blog post** — 2000+ words, SEO-optimized.
   Commit and push to your content repo.

4. **Engage in communities** — Find 3+ threads where people ask
   about [your domain]. Add genuine value. Link to your product
   ONLY if directly relevant.

## Log:
Append actions (with URLs/links) to memory/marketing-actions.md.
Include: what you did, links, expected impact.

DO NOT write a strategy proposal. DO things.
```

### Outreach Agent

**Before:**
```
OUTREACH SHIFT: Research partnership opportunities. Identify
potential affiliates or collaborators. Write a partnership strategy.
```

**After:**
```
OUTREACH SHIFT — OUTBOUND ACTIONS REQUIRED

You MUST send at least 2 cold outreach emails AND submit to at least
1 directory. Reports alone = failure.

## Required Actions:

### 1. Send 2+ outreach emails (MANDATORY)
[exact tool/command to send email]

Find prospects by:
- Searching for recent launches, community posts, forum threads
- Check if sites have visible contact emails
- Check your outreach log so you don't duplicate

Email rules:
- Lead with insight about THEIR business, not yours
- Under 80 words body
- Soft CTA: link to your free tool or resource
- PAS framework (Problem-Agitate-Solve)

### 2. Submit to 1+ directory (MANDATORY)
- Check your directory log for done/blocked
- Log results

## Log:
Append ALL actions (emails sent, directories submitted) to
memory/outreach-actions.md with addresses, subjects, URLs.
```

## The Restructuring Process

### Step 1: List your shifts
Write down every recurring agent session (cron jobs, heartbeat tasks, shifts).

### Step 2: Categorize each shift

| Category | Action Required? | Example |
|---|---|---|
| **Outbound** | Yes — must produce external output | Marketing, Outreach, Research |
| **Operational** | Action = system check (fine as-is) | Ops, Security, DevOps |
| **Analytical** | Depends — pair with action when possible | Analyst, Data |
| **Creative** | Yes — output must ship, not sit in a file | Design, Content |

### Step 3: For each outbound shift, apply the template

1. Add "OUTBOUND ACTIONS REQUIRED" header
2. Set minimum action count (start with 1-2, increase over time)
3. List specific actions with exact tools/commands
4. Add proof-of-action logging requirement
5. Add "Reports alone = failure" guardrail
6. Keep research/analysis as input TO actions, not standalone

### Step 4: For analytical shifts, find the action pair

- "Analyze conversion funnel" → "Analyze funnel AND write 3 A/B test hypotheses with implementation steps"
- "Review competitor pricing" → "Review pricing AND draft a pricing comparison blog post"
- "Track metrics" → "Track metrics AND flag any metric that crossed a threshold with recommended immediate action"

### Step 5: Test and iterate

Run the restructured shift once. Check:
- Did it produce external output?
- Can you find proof (URLs, IDs, sent emails)?
- Did the quality of the action meet your bar?
- Was the research/analysis still useful, or did it get skipped?

Adjust action count and specificity based on results.

## Transition Tips

- **Don't remove research entirely.** Research that serves an action is valuable. Research that sits in a file is waste.
- **Start with 1 required action.** Agents need to learn the pattern. Ramp up to 2-3 over a week.
- **Provide exact commands.** Agents are much more likely to act when you hand them the exact CLI command, API call, or script to use.
- **Log everything with proof.** URLs and IDs are non-negotiable. "I posted" without a link is fiction.
- **Accept imperfect action over perfect planning.** A mediocre tweet that's actually posted beats a brilliant strategy doc that nobody reads.
