# APPLICATION LOG
# File: upwork-auto-apply/.upwork/APPLICATION_LOG.md
# Version: 1.0.3
#
# This file is maintained automatically by ProposalAI.
# Do not edit manually unless correcting an error.
#
# Privacy notice: This file stores your proposal drafts, job details, and
# client information locally on your machine. Do not share this file publicly
# or upload it to version control (GitHub, GitLab, etc).
#
# Written by: ProposalAI (appends new entries during sessions)
# Read by:    ProposalAI (loads at session start) and pre-apply-check.sh (duplicate check)
# Location:   upwork-auto-apply/.upwork/APPLICATION_LOG.md

---

## ENTRY FORMAT

Each application entry uses this exact format:

---
JOB_ID:         [Upwork Job ID from the URL]
TITLE:          [Job title as posted on Upwork]
CATEGORY:       [Web Dev / Automation / API / Data / Other]
BUDGET:         [$X fixed   OR   $X to $X per hour]
CLIENT_RATING:  [X.X out of 5.0]
CLIENT_SPEND:   [$X total spent on Upwork]
PAYMENT:        [Verified / Not Verified]
POSTED:         [YYYY-MM-DD]
APPLIED:        [YYYY-MM-DD]
STATUS:         [draft / applied / interviewing / hired / rejected / closed]
HOOK_USED:      [Hook ID from PROPOSAL_VAULT.md — example: WD-001]
SCORE:          [Job score from criteria matrix — example: 78 out of 100]
PROMOTED:       [yes / no — was this hook promoted to the vault?]

PROPOSAL:
"""
[Full proposal text as drafted by ProposalAI — review and edit before submitting on Upwork]
"""

OUTCOME_NOTES:
[Leave blank at draft time. Fill in when the status changes.]
---

---

## STATUS DEFINITIONS

draft        — Proposal was drafted but not yet submitted on Upwork
applied      — User confirmed the proposal was submitted on Upwork manually
interviewing — Client responded and an interview or conversation started
hired        — Contract was awarded
rejected     — Application was declined or received no response after 14 days
closed       — Job was closed or filled before a decision was made

---

## ACTIVE ENTRIES

ProposalAI appends new draft entries below this line.

[no entries yet]

---

## CLOSED ENTRIES

ProposalAI moves resolved entries here to keep the Active section clean.

[no entries yet]

---

## DISQUALIFICATION LOG

Jobs that failed the Pre-Flight Filter. Logged for transparency.
Format: DATE | JOB_ID | TITLE | REASON

[no entries yet]

---

## RUNNING TOTALS

ProposalAI updates these at the end of each session.

total_drafted:         0
total_submitted:       0
total_disqualified:    0
currently_active:      0
interviewing:          0
hired:                 0
rejected:              0
interview_rate:        0 percent
close_rate:            0 percent
hooks_promoted:        0
last_session:          [never]

---

# File: upwork-auto-apply/.upwork/APPLICATION_LOG.md
# Version: 1.0.3
