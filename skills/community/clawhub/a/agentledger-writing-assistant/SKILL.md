---
name: writing-assistant
version: "1.0.0"
url: https://github.com/theagentledger/agent-skills
description: AI writing partner for solopreneurs and content creators. Drafts, edits, and improves written content — emails, blog posts, newsletters, social captions, and reports. Maintains your voice, adapts to format and audience, and helps you produce polished content faster. Integrates with content-calendar, inbox-triage, and solopreneur-assistant skills.
tags: [writing, content, editing, drafting, newsletter, email, productivity]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
---

# Writing Assistant
**by [The Agent Ledger](https://theagentledger.com)**

*Your AI writing partner. Draft faster, edit sharper, publish with confidence.*

---

## What This Skill Does

This skill turns your agent into a writing collaborator that:

- **Drafts** content from a brief or bullet points
- **Edits** existing drafts for clarity, tone, and structure
- **Improves** weak sections without rewriting what's working
- **Adapts** to your voice and audience (not generic AI output)
- **Stores** writing style notes so every output sounds like *you*

It handles emails, blog posts, newsletter issues, social captions, LinkedIn posts, cold outreach, and long-form reports — with consistent quality across all formats.

---

## Setup (5 Steps)

### Step 1: Add to AGENTS.md

Paste into your `AGENTS.md` standing instructions:

```markdown
## Writing Assistant (Agent Ledger Skill)

I help draft, edit, and improve written content. Before writing anything,
I check `writing-state.md` for voice notes, style preferences, and past work.

Default behavior:
- Match the user's voice unless explicitly told to adjust
- Ask for audience and goal if not provided for long-form drafts
- Never use filler phrases ("Certainly!", "Great question!", "Delving into")
- Keep sentences active and direct
- Prefer concrete over abstract; specific over vague
- Always offer the user a chance to revise before finalizing

On request, I can: Draft, Edit, Tighten, Expand, Change tone, Add a CTA, Create variants
```

### Step 2: Create Your Voice Profile

Create `writing-state.md` in your workspace root:

```markdown
# Writing State

## Voice Profile
- **Tone:** [e.g., Direct and conversational, slightly sardonic]
- **Sentence style:** [e.g., Short sentences. Varied rhythm. No padding.]
- **Vocabulary:** [e.g., Plain English. Avoid jargon. Exception: industry terms with audience familiarity]
- **POV:** [e.g., First person singular for blog/newsletter; second person for instructional]
- **Things I never say:** [e.g., "leverage", "synergy", "unlock your potential"]
- **Things I often say:** [e.g., "Here's the thing", "The short version:", "Worth noting:"]

## Audiences
- **Newsletter:** [Describe reader — e.g., solopreneurs building AI-assisted businesses, 25-45]
- **Email (cold):** [Describe context — e.g., B2B, product-led, no hard sell]
- **Social (LinkedIn):** [e.g., Professional but human, no corporate-speak]
- **Blog:** [e.g., Practitioners who want to implement, not just learn]

## Format Preferences
- **Email subject lines:** [e.g., Under 50 chars, curiosity-driven, no clickbait]
- **CTA style:** [e.g., One CTA per piece, specific action, no "click here"]
- **Paragraph length:** [e.g., 2-4 sentences max for web content]
- **Headers:** [e.g., Question-based or action-based, never "Introduction"]

## Content Archive
_Titles of recent pieces for style reference (agent updates this over time):_
- [2026-03-07] — "[Title]" — [Format] — [Brief note on tone/approach]
```

**Fill in your real preferences.** The more specific, the better. The agent will improve this file over time as you give feedback.

### Step 3: Test With a Simple Draft

Run this prompt to verify setup:

```
Write a 3-sentence email reply to a client asking for a project status update.
The project is on schedule. Check writing-state.md for tone first.
```

If the output sounds like you, you're set. If not, update your voice profile.

### Step 4: Configure Integrations (Optional)

If you use other Agent Ledger skills, add these to your `AGENTS.md`:

```markdown
## Writing ↔ Content Calendar
When I complete a draft marked as "scheduled" in content-calendar, I update
the piece status to "Draft Complete" in the pipeline.

## Writing ↔ Inbox Triage
When inbox-triage flags an email needing a reply, I can draft the reply
on request. I never auto-send — I always present the draft for review first.
```

### Step 5: Add to HEARTBEAT.md (Optional)

If you want periodic writing prompts or reminders:

```markdown
## Writing Assistant Checks
- Flag any content-calendar items in "Overdue Draft" status
- If last piece was published >7 days ago, note it as a gentle reminder
```

---

## Core Usage Patterns

### Draft From a Brief

```
Draft [FORMAT] about [TOPIC].
Audience: [WHO]
Goal: [WHAT YOU WANT THEM TO DO OR FEEL]
Length: [APPROXIMATE]
Key points to cover: [BULLETS]
```

**Example:**
```
Draft a LinkedIn post about why most AI agent setups fail within a week.
Audience: Solopreneurs who've tried AI tools but given up.
Goal: Curiosity — make them want to read my newsletter.
Length: ~150 words.
Key points: blank AGENTS.md, no memory, no personality.
```

---

### Edit an Existing Draft

```
Edit this draft. Focus on [clarity / tone / structure / flow / all].
Keep what's working. Don't rewrite sections that sound good already.

[PASTE DRAFT]
```

**Editing modes you can request:**
- `Tighten` — cut 20-30% without losing meaning
- `Elevate` — improve word choice and sentence flow
- `Punch up the opening` — fix weak first paragraphs
- `Fix the ending` — most drafts end weakly; this repairs that
- `Check for passive voice` — flag and fix passive constructions
- `Add a CTA` — append a clear call to action
- `Match my voice` — rewrite a section you've pasted that sounds off

---

### Newsletter Issue Drafting

```
Draft newsletter issue [#N]: "[WORKING TITLE]"
- Main topic: [WHAT IT'S ABOUT]
- Reader takeaway: [WHAT THEY SHOULD KNOW OR DO]
- Sections needed: [e.g., intro hook, main content, one tip, CTA]
- Previous issue recap (optional): [BRIEF SUMMARY]
- Tone: [e.g., Same as usual — check writing-state.md]
```

Newsletter format template (agent will adapt):

```
SUBJECT: [Subject line — 3 variants]

---

[HOOK — 2-3 sentences that open with a story, question, or observation]

[MAIN CONTENT — broken into short sections with subheads]

[PRACTICAL TAKEAWAY — specific action or insight they can use today]

[CLOSING — brief, personal, connects back to hook]

[CTA — one clear action: reply, click, share]

---
[FOOTER — unsubscribe link placeholder, legal boilerplate if needed]
```

---

### Cold Email / Outreach Drafting

```
Draft a cold email to [WHO] about [WHAT].
Context: [Why I'm reaching out, what I want]
Offer / value prop: [What's in it for them]
CTA: [Specific ask — meeting, reply, click]
Tone: [e.g., Peer-to-peer, not salesy]
Length: Under [N] words.
```

**Cold email rules the agent follows by default:**
1. No generic openers ("I hope this finds you well")
2. Lead with their situation, not your pitch
3. One clear CTA — never two asks
4. Subject line that doesn't reveal it's a pitch
5. Under 150 words unless the product complexity demands more

---

### Social Caption Variants

```
Write [N] variants of a [LinkedIn / Twitter / Instagram] caption for:
Topic: [WHAT]
Angle: [e.g., Contrarian take / story / tip / question]
Include: [Hashtags yes/no] [CTA yes/no]
Max length: [CHARACTERS OR "Platform default"]
```

---

### Repurpose Existing Content

```
Repurpose this [blog post / newsletter / transcript] into:
- A [LinkedIn post / Twitter thread / email / summary]
Extract the core insight, don't just summarize. Write for [PLATFORM AUDIENCE].

[PASTE CONTENT]
```

---

## Style Quality Checklist

The agent uses this internally before finalizing any draft. You can also request an explicit check:

```
Run a style quality check on this draft:
[PASTE DRAFT]
```

**Checklist (what the agent checks):**

| Check | Pass Criteria |
|-------|--------------|
| Voice match | Reads like writing-state.md voice profile |
| No filler phrases | Zero "Certainly!", "Great question!", "Leverage", etc. |
| Opening strength | First sentence earns attention |
| Active voice | < 15% passive constructions |
| Paragraph length | ≤ 4 sentences for web; longer allowed for long-form |
| One CTA only | Zero pieces end with two or more asks |
| Concrete over abstract | At least one specific example or number |
| Ending lands | Final sentence resonates, not "Thanks for reading!" |

---

## Format Reference

### Email
- Subject line: ≤ 50 characters preferred; A/B test subjects for campaigns
- Opening: No pleasantries; start with the reason for writing
- Body: One topic per email; use short paragraphs
- Sign-off: First name only for casual; full for formal

### Blog Post
- Hook: First 2 sentences must earn the scroll
- H2s: Question-based or action-based ("Why X fails" / "How to X")
- Length: 600-1,200 words for instructional; 1,500-3,000 for deep-dives
- Conclusion: Summary + next step, not "In conclusion"

### Newsletter
- Subject line tests: Curiosity vs. direct benefit — test both
- Reader contract: One core insight per issue, not five
- Tone: Consistent voice issue-to-issue (check archive in writing-state.md)
- Cadence language: Always welcome late subscribers with brief context

### LinkedIn
- Opening line: No context-setting — start with the hook
- Length: 150-300 words performs well for text posts
- Line breaks: Single sentences preferred for mobile readability
- Hashtags: 3-5 relevant; avoid generic (#AI, #marketing spam)

### Twitter / X
- Lead tweet: The whole point, not a teaser
- Thread structure: Each tweet stands alone; thread adds depth
- Thread length: ≤ 8 tweets for most topics
- Final tweet: CTA or open question

---

## Customization

### Adjust Tone Per Format

Add to your `writing-state.md`:
```markdown
## Per-Format Tone Overrides
- LinkedIn: 10% more formal than usual voice
- Twitter: Sharper, more direct; punchlines allowed
- Cold email: Peer-to-peer; match their seniority level
- Newsletter: Warmest, most personal voice
```

### Block Phrases / Words

```markdown
## Words I Never Use
- leverage, synergy, unlock, empower, journey, passion
- "It's important to note that"
- "In today's fast-paced world"
- Any sentence starting with "I" in cold emails
```

### Revision Tracking

Request a tracked revision log:
```
Edit this draft and list every change you made with a one-line reason.
[PASTE DRAFT]
```

### Confidence Ratings

Request confidence scoring on subject lines or headlines:
```
Write 5 subject line options for [TOPIC].
Score each 1-10 for: curiosity, clarity, click-through likelihood.
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Output sounds generic | Add more specifics to voice profile in writing-state.md; provide an example of your writing |
| Too long / too short | Specify word count explicitly; add length preference to writing-state.md |
| Wrong tone | Run "Match my voice" edit with a sample of your actual writing |
| CTAs are weak | Specify exact action in brief; paste examples of CTAs you like |
| Openings are flat | Request "Punch up the opening" separately; give the agent 3 hook options to choose from |
| Inconsistent between sessions | Ensure writing-state.md is being checked; add to AGENTS.md standing instructions |

---

## Integration Map

| Skill | How They Connect |
|-------|-----------------|
| **content-calendar** | Agent updates pipeline status when drafts complete |
| **inbox-triage** | Draft replies to flagged emails on request |
| **solopreneur-assistant** | Business writing (proposals, reports, strategy docs) |
| **research-assistant** | Research → writing pipeline: research brief feeds into draft |
| **newsletter** | Newsletter drafting with issue archive in writing-state.md |
| **daily-briefing** | Include writing reminders in daily briefing |

---

## Privacy & Security Note

- Writing drafts may contain client names, business details, or sensitive content. Store drafts in local workspace only.
- Never auto-publish or auto-send. Every draft requires your review before it leaves your machine.
- writing-state.md may contain proprietary information. Exclude from any public repos.

---

*Writing Assistant is part of the Agent Ledger Skills Suite — free, open-source tools for solopreneurs building AI-assisted businesses.*

*Subscribe at [theagentledger.com](https://theagentledger.com) for new skills, deep dives, and the premium guide on building production-grade AI agent setups.*

*License: CC-BY-NC-4.0 | Free to use and adapt for non-commercial purposes.*

> *DISCLAIMER: This skill was created by an AI agent. It is provided "as is" for informational and educational purposes only. It does not constitute professional, financial, legal, or technical advice. Review all generated files before use. The Agent Ledger assumes no liability for outcomes resulting from use. Use at your own risk.*
