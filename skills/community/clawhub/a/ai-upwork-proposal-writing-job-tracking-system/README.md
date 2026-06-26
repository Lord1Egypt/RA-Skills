# AI Upwork Proposal Writing & Job Tracking System
**Version**: 1.0.3 | **Folder**: upwork-auto-apply/

A local AI writing assistant that helps freelancers filter Upwork job listings, draft personalized proposals, track applications, and improve over time by learning from winning proposals.

---

## How It Works

You paste job listings into the chat. The assistant filters out bad leads, drafts a personalized proposal for each qualified job, and saves everything to a local log file. You review each draft, edit if needed, and paste it into Upwork yourself. The assistant does not connect to Upwork or submit anything automatically.

---

## What Makes This Different From Writing Proposals Manually

**Problem 1: You waste time on bad jobs.**
The Pre-Flight Filter checks every listing against your personal rules before drafting anything. Unverified payment, low client ratings, budgets below your floor, and blacklisted keywords are all caught automatically. You see exactly why each job was skipped.

**Problem 2: Every proposal starts from zero.**
The Proposal Vault stores your winning hooks. Every time you report an interview or hire, the assistant extracts what worked from that proposal and saves it to the vault. Future proposals are built from your own proven patterns, not generic templates.

**Problem 3: You forget what you applied to.**
Every draft is saved to a local log file with the job details, the full proposal text, and the current status. You always know what you have applied to and what the outcome was.

---

## The Four-Part Proposal Structure

Every draft follows a structure built for Upwork conversion:

1. **Hook** — Opens with a specific detail from the job post. Never starts with "I" or "Hi."
2. **Credibility Bridge** — One quantified result from your past work that matches the client's need.
3. **Solution Preview** — One or two concrete ideas showing how you would approach the project.
4. **Soft CTA** — Invites a conversation, not a commitment.

---

## The Memory Promotion Protocol

When you tell the assistant "I got an interview for Job ID 1234," it finds the winning proposal, extracts the hook and structure that worked, and adds it to your Proposal Vault tagged with the job category and budget range.

The next time a similar job appears, the assistant draws from that proven pattern. The quality of your proposals improves automatically as you win more work.

---

## System Requirements

This skill runs locally. The pre-apply-check.sh script uses standard tools that are already installed on macOS and Linux:
- bash (version 3.2 or later)
- awk (for decimal number comparison)
- grep (for duplicate application detection)

No additional software needs to be installed. No internet connection is required.

---

## File Structure

All files are inside the upwork-auto-apply/ folder. No files outside this folder are read or written.

```
upwork-auto-apply/
├── SKILL.md                    (agent instructions)
├── README.md                   (this file)
├── assets/
│   ├── FREELANCER_PROFILE.md   (fill this in first — your skills, rates, blacklist)
│   ├── IDEAL_JOB_CRITERIA.md   (job scoring weights)
│   └── PROPOSAL_VAULT.md       (winning hooks — grows with every win)
├── scripts/
│   └── pre-apply-check.sh      (job filter — uses bash and awk only)
└── .upwork/
    └── APPLICATION_LOG.md      (your local application history)
```

Privacy note: APPLICATION_LOG.md stores your proposal drafts and job details locally on your machine. This file may contain personal information. Do not share it publicly or upload it to version control.

---

## Setup

**Step 1**: Open upwork-auto-apply/assets/FREELANCER_PROFILE.md and fill in your skills, hourly rate, minimum budget, proof points, and blacklist keywords.

**Step 2**: Open upwork-auto-apply/assets/IDEAL_JOB_CRITERIA.md and adjust the scoring weights and budget thresholds to match your goals.

**Step 3**: Start a session and say: "Help me draft proposals for these jobs" — then paste in job listings from Upwork.

---

## Trigger Commands

| What you say | What the assistant does |
|---|---|
| "Help me draft proposals for these jobs" | Filters listings, scores them, writes drafts |
| "I got an interview for Job ID [X]" | Promotes winning hook to vault, updates log |
| "Mark Job [X] as hired" | Updates status, promotes hook |
| "Show me my proposal stats" | Dashboard showing rates, active bids, vault size |

---

## What This Tool Does and Does Not Do

| Does | Does not do |
|---|---|
| Draft personalized proposals locally | Submit to Upwork automatically |
| Filter jobs against your rules | Connect to the Upwork API |
| Track applications in a local file | Log into your account |
| Learn from your interview wins | Access any external service |
| Store your full proposal history | Access files outside upwork-auto-apply/ |

---

*Version 1.0.3 | MIT-0 License | No network access | No external dependencies*
*Folder: upwork-auto-apply/ | Script tools: bash, awk, grep*
