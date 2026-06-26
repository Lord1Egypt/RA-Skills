---
name: freelance-proposal-writer
description: Write high-converting freelance proposals from job postings (Upwork, Toptal, Freelancer, etc). Given a job URL or pasted description, analyzes the client's real pain point, scores the fit, and writes a 200-word proposal that leads with the solution — not your resume. Saves connects and increases win rate.
argument-hint: [job URL or paste job description]
allowed-tools: Read, Bash, WebSearch
metadata:
  version: "1.0.0"
  author: "clawsonnet"
  tags: ["freelance", "upwork", "proposal", "sales", "client", "outreach"]
---

# Freelance Proposal Writer

## Why This Exists
Generic proposals waste connects. This skill crafts targeted proposals that lead with the client's problem, not your resume. 180-220 words that get responses.

## Setup

Edit the `MY_STACK` section below to match your skills. This runs once:

```
MY_STACK:
- Frontend: [your frontend skills]
- Backend: [your backend skills]
- AI/Automation: [your AI/automation stack]
- Rate: [your rate range — e.g., $65-100/hr or project-based]
```

## Process

### Step 1: Extract Job Details

From `$ARGUMENTS`:
- If URL: use WebSearch or Bash to fetch page content
- If pasted text: parse directly

Extract:
- Client's stated problem (what they're asking for)
- Client's real problem (what they actually need — often different)
- Budget (hourly vs fixed)
- Timeline
- Tech stack specified or implied
- Client background (company type, size, spend history if visible)

### Step 2: Score the Opportunity

Quick fit score (skip if < 6/10):
- Stack match: /3 (2+ = strong match)
- Budget viable: /2 (meets your floor)
- Client quality: /2 (some platform history, reasonable expectations)
- Problem solvable: /2 (not vague "build me a startup" type requests)
- Timeline realistic: /1

If score < 6: output `SKIP — [specific reason]` and stop.

### Step 3: Identify the Hook

The first line is everything. Find the client's most pressing pain:
- "You're losing users because [X]"
- "The bug you described is caused by [Y], here's the fix"
- "I've built exactly this for [similar context] — here's what I learned"

Never start with "Hi, I'm [name]" or list your skills first.

### Step 4: Write the Proposal

Target: 180-220 words. Structure:
```
[HOOK — 1-2 sentences. Lead with their problem or a direct solution]

[SOLUTION — 2-3 sentences. Concrete approach. Specific tech choices + why]

[PROOF — 1-2 sentences. Closest relevant thing you've built. No fluff]

[TIMELINE & CTA — 1-2 sentences. Realistic estimate + clear next step]
```

Tone: confident, direct, no buzzwords. Write like texting a peer.

**Avoid:** "I am a highly experienced developer", "I would love to help", "I am very passionate about", generic portfolio links without context.

### Step 5: Output

Produce:
1. The fit score with breakdown
2. The proposal text (ready to paste)
3. One optional follow-up question to add at the end (optional, if it would help)

## Example Output Format

```
FIT SCORE: 8/10
- Stack: 3/3 (Next.js + Supabase exact match)
- Budget: 2/2 ($75/hr = your minimum)
- Client: 2/2 ($5k spend history, US company)
- Problem: 2/2 (specific auth bug, clear scope)
- Timeline: 1/1 (2-week estimate is realistic)

PROPOSAL:
[180-220 word proposal here]

OPTIONAL QUESTION: "Are you open to a 1-hour paid discovery call to confirm the scope before the full project kicks off?"
```
