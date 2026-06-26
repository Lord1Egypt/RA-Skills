---
name: claim-evidence-timeline-builder
description: "Build a clear chronological timeline and proof index from user-provided events and evidence. Use when the user needs to explain what happened with supporting proof, identify gaps, and draft a concise factual summary without legal advice."
---
# Claim Evidence Timeline Builder

## Purpose

Turn scattered events, messages, documents, screenshots, receipts, or notes into a clear chronological timeline with a proof index, gaps list, and concise summary. The output should help the user explain what happened accurately and calmly.

This is a prompt-only factual organization workflow. It is not legal advice, financial advice, professional advocacy, or a prediction of outcomes.

## Use This Skill When

Use this skill when the user needs to organize a claim, dispute, complaint, incident, warranty issue, workplace matter, school matter, insurance packet, platform appeal, customer support case, or personal record and wants to show:

- What happened.
- When it happened.
- What proof supports each event.
- What is still missing.
- A short factual summary that separates facts from interpretation.

Do not use it to fabricate events, invent evidence, coach deception, impersonate a professional, threaten unsupported action, or make legal conclusions.

## Safety Boundary

- Do not provide legal advice, legal strategy, or predictions about liability, eligibility, damages, penalties, or case outcomes.
- Do not decide whether a claim is valid, enforceable, or likely to win.
- Use only user-provided events, documents, messages, screenshots, records, and descriptions. Do not invent proof or facts.
- Separate facts, user interpretation, and open questions.
- Flag unsupported statements and ask what proof exists instead of strengthening them rhetorically.
- Encourage the user to follow official instructions, deadlines, and document submission rules for the relevant organization when those rules are available.
- For legal threats, court deadlines, police reports, serious injury, immigration, employment termination, housing loss, insurance denial, debt collection, or large financial stakes, recommend consulting an appropriate qualified professional or official resource.
- Minimize sensitive data. Use labels, redactions, partial identifiers, and filenames instead of full account numbers, ID numbers, passwords, one-time codes, or credentials.

## Best Inputs

Ask for only what is needed. If information is missing, build the timeline with placeholders and a gaps list.

- The situation type and the audience for the timeline.
- Key events with dates or approximate dates.
- People, organizations, order numbers, ticket numbers, policy numbers, or case identifiers, preferably redacted.
- Proof the user has, such as emails, texts, screenshots, receipts, contracts, photos, logs, forms, shipping records, medical visit summaries, police report numbers, support tickets, or witness notes.
- What the user wants corrected, answered, reimbursed, reviewed, or acknowledged.
- Any submission deadline or format requirement supplied by the user.

## Workflow

1. **Clarify the purpose.** Identify the audience, decision to be made, requested outcome, deadline, and any format limits.
2. **Collect events.** Capture each event as stated by the user with date, time if known, actor, location or channel, action, and source.
3. **Sort by time.** Put events in chronological order. Use approximate labels such as "early March" or "before 2026-04-12" when exact dates are unknown.
4. **Attach proof.** Assign each piece of user-provided evidence a proof ID, then connect proof IDs to the events they support.
5. **Separate fact from interpretation.** Mark what is directly supported, what is the user's interpretation, and what remains unknown.
6. **Mark gaps.** Identify missing dates, missing documents, unclear sequence points, unsupported claims, contradictions, and items that need verification.
7. **Write the concise summary.** Draft a short, factual summary that explains the sequence, the issue, the supporting proof, and the requested next step.
8. **Prepare next-step questions.** List the smallest set of follow-up questions or documents that would materially strengthen the timeline.

## Output Format

Return the artifact in this order.

### 1. Timeline Purpose

| Field | Detail |
|---|---|
| Audience | |
| Topic or claim | |
| Requested outcome | |
| Deadline or format rules | |
| Boundary note | Facts organized from user-provided information only; not legal advice. |

### 2. Chronological Timeline

| Date or time | Event | Source or proof ID | Fact, interpretation, or unclear | Notes |
|---|---|---|---|---|
| | | | | |

Rules for this section:

- Use exact dates when provided.
- Use approximate labels when exact dates are missing.
- Do not fill in unknown dates or facts from assumption.
- Keep interpretations clearly labeled.

### 3. Proof Index

| Proof ID | Evidence item | What it supports | Provided by user? | Notes or redactions |
|---|---|---|---|---|
| P1 | | | Yes | |

Only include evidence the user says exists or has provided. If evidence is needed but not available, put it in the gaps list instead.

### 4. Gaps and Follow-Up List

| Gap | Why it matters | How to fill it | Priority |
|---|---|---|---|
| | | | |

Include missing dates, missing proof, unclear actors, contradictions, unsupported statements, submission rules, and sensitive details that should be redacted.

### 5. Fact vs. Interpretation Notes

Group statements as:

- Directly supported facts.
- User interpretation or belief.
- Unknown or needs verification.

Rewrite loaded or accusatory wording into neutral factual language when possible.

### 6. Concise Summary

Write a short paragraph or bullet summary suitable for the intended audience. It should include:

- The core sequence.
- The key supporting proof IDs.
- The specific requested action or response.
- A neutral statement of what remains unresolved.

### 7. Submission Checklist

Provide a short checklist for packaging the timeline:

- Redact sensitive identifiers.
- Name files clearly.
- Keep originals unchanged.
- Include proof IDs in filenames or notes.
- Follow the recipient's official submission rules and deadlines if supplied.
- Save a copy of what was submitted and when.

### 8. Open Questions

End with concise questions that would improve accuracy or completeness.

## Example Prompts

- "I need to build a timeline for a warranty claim on my laptop. I have receipts, repair emails, and support chat logs from the past four months."
- "Help me organize everything that happened with my landlord dispute into a clear timeline. I have texts, emails, photos, and a lease."
- "I'm putting together evidence for a chargeback. I have order confirmations, shipping notices, and six emails with customer support. Turn this into a timeline with proof IDs."

## Style

- Be precise, neutral, and chronological.
- Preserve uncertainty instead of smoothing it over.
- Prefer "the user reports" or "the record shows" when appropriate.
- Avoid legal labels unless the user provided them as quoted language from an official document.
- Do not exaggerate, threaten, or infer intent without evidence.
- Keep sensitive identifiers redacted or abbreviated.
