---
name: advisor-finder
description: Find and analyze potential academic advisors, supervisors, or faculty for a target university, school, department, or research direction. Use when the user asks to find professors/mentors/PI/faculty, screen advisors for master's or PhD applications, compare faculty fit, identify recent papers, or rank who is most worth contacting based on research match, activity, and public profile evidence.
---

# Advisor Finder

Find candidate advisors for a target university or department, verify what they actually work on, and rank who is most worth contacting.

## Core objective

Turn a vague request like “help me find professors doing LLMs at Zhejiang University Software College” into a defensible shortlist with evidence.

The skill must not stop at listing names. It must:
1. find faculty,
2. verify research direction from primary evidence,
3. inspect recent papers and public profiles,
4. judge fit against the user's background or target,
5. output a ranked shortlist with reasons.

## Inputs to extract

Identify as many of these as the user already gave:
- university name
- school / department / institute name
- target research direction
- degree goal: master's / PhD / RA / visiting / broad exploration
- user background keywords
- region preference
- faculty seniority filter: professor only / professor + associate professor / all faculty
- paper time window: 2 / 3 / 5 years
- shortlist size wanted

If key inputs are missing, make the smallest reasonable assumption and continue. Ask follow-up only when the ambiguity would materially change the result.

## Evidence hierarchy

Prefer evidence in this order:
1. official university / department / lab pages
2. faculty personal homepage
3. structured research directories or datasets with strong CS coverage, such as CSrankings, when applicable
4. Google Scholar / Semantic Scholar / DBLP / OpenReview / official publication page
5. lab member pages, project pages, recent talk pages
6. third-party pages only as backup

Read `references/github-datasets.md` when the official school site is weak and the target field is computer science or nearby areas.

Do not treat one old paper as proof of a current research direction. Look for repeated recent evidence.

## Workflow

### Step 1: Lock the official target page

Find the official university page and then the official school / department / faculty directory page.

Record:
- official school name
- official faculty directory URL
- whether the page is complete or obviously partial

If the school is a top university or the site is messy, read `references/top-university-sites.md` first for likely official entry points.

If the target is a major Chinese university and the user is looking for economics/management, computer science, software, or data science related schools, also read `references/china-top-university-hints.md` for common official entry patterns.

If the official directory is poor, supplement with official lab pages and faculty personal pages.
If the site blocks scraping or key fields are hidden, follow `references/site-failure-playbook.md` instead of guessing.

### Step 2: Build the faculty pool

Collect candidate faculty members with at least:
- name
- title
- homepage URL if available
- email if publicly listed
- research keywords from official page if available

Before moving on, assign a pool completeness label:
- High: official faculty pool looks mostly complete
- Medium: official pool exists but clearly partial
- Low: official pool is fragmented and must be reconstructed from labs + homepages + external structured datasets

If the target field is computer science, AI, CV, NLP, systems, ML, HCI, security, or robotics, and the official faculty pool is weak, consult `references/github-datasets.md` for CSrankings-style recovery.

Exclude obvious non-target roles unless the user asked broadly:
- administrative staff
- purely teaching staff without research role
- postdocs / students unless specifically requested

### Step 3: First-pass direction filter

Use official profile text, homepage text, and lab descriptions to do a coarse filter.

Examples:
- for LLM: large language model, LLM, foundation model, NLP, agent, multimodal, reasoning
- for CV: computer vision, vision-language, image understanding, 3D vision
- for systems: distributed systems, databases, systems for ML, networking

Keep borderline candidates for verification rather than dropping them too early.

### Step 4: Verify recent research line

For each shortlisted candidate, inspect recent papers and profile evidence.

Minimum checks:
- recent paper topics in the last 2 to 5 years
- whether the target direction appears repeatedly
- whether the person seems active recently
- whether the person looks central to the work or only occasionally adjacent

Use paper-search or scholar-style skills if available. Use paper-parse only after a specific paper is worth reading deeply.

### Step 5: Build the advisor profile

For each candidate, write a compact profile covering:
- main research line
- target-direction relevance
- recent activity level
- style tendency: theory / method / engineering / application
- likely contact value
- uncertainty level

Use `references/scoring-template.md` as a soft rubric. Do not fake precision, but do make the ranking logic explicit.

### Step 6: Match against the user

If the user gave background info, compare:
- skill overlap
- topic overlap
- methodological overlap
- likely entry barrier
- whether the user can plausibly write a credible outreach email

If the user gave no background, rank only by target-direction fit and activity.

### Step 7: Rank and output

Produce a shortlist with explicit ranking bands:
- Priority A: strong fit, active, worth contacting early
- Priority B: plausible fit, worth contacting
- Priority C: weak or uncertain fit, backup only

## Scoring guide

Use soft scoring, not fake precision. Judge each dimension as High / Medium / Low or 0-5.

Suggested dimensions:
- direction match
- recent activity
- evidence strength
- user-background fit
- outreach value

Do not hide uncertainty. If evidence is weak, say so.

## Required output structure

Start with a brief scope line:
- target university
- department
- direction
- time window

Then output a ranked table or bullet list.

For each faculty member include:
- Name
- Title
- School / Department
- Homepage
- Email if public
- Research summary in plain Chinese
- Recent evidence: 2-4 papers or profile facts
- Match assessment
- Risks / uncertainty
- Recommendation: Priority A / B / C

Then end with:
- top 3 recommended contacts
- why they are top 3
- what to do next
- whether the site evidence quality was High / Medium / Low

## What to avoid

Do not:
- rank only by fame
- infer current direction from one old famous paper
- confuse coauthors with the actual faculty member
- treat non-official pages as authoritative when official pages exist
- overclaim whether a faculty member is recruiting

## Escalation points

If the user asks for deeper analysis of one professor:
- identify one or more recent representative papers
- use paper-parse on the most relevant paper
- update the advisor profile with paper-level evidence

If the user asks for many schools:
- handle one school at a time
- keep a structured table across schools

If a school website is especially bad:
- do not force a fake confident answer
- downgrade evidence strength
- produce a provisional shortlist first
- note exactly what still needs verification

## Output style

Write in direct Chinese.
Prefer short, useful judgments over inflated academic prose.
The user should be able to read the result and immediately know who is worth contacting first and why.
