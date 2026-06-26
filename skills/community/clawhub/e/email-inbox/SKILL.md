---
name: email-inbox-triage
description: summarize, triage, and draft actions for incoming email. use when the user wants chatgpt to check an inbox, identify important unread messages, group emails by urgency or topic, extract action items, prepare reply drafts, or help process new mail with gmail or another connected mail source.
---

# Email Inbox Triage

## Overview
Use this skill to process incoming email in a consistent way: check the inbox, identify what matters, summarize the important parts, and prepare the next action.

## Core workflow
Follow this sequence unless the user asks for only one specific step.

1. Identify the mailbox source.
   - Prefer a connected mail tool such as Gmail when available.
   - If no connector is available, ask the user to provide exported emails, pasted email text, or screenshots.

2. Collect the target messages.
   - If the user says "new mail" or "recent email", focus on unread or recent inbox messages first.
   - If the user names a sender, company, subject, or date range, filter to those messages.
   - If the user asks for "important" email, infer importance from sender, urgency, deadlines, invoices, approvals, customer requests, and direct asks.

3. Triage the messages.
   - Classify each message into one of these buckets:
     - urgent
     - needs reply
     - needs review
     - informational
     - low priority
   - Detect explicit deadlines, meeting times, payment requests, approvals, and follow-up asks.

4. Produce a useful output.
   Default to this structure unless the user asks for another format:

   ### Inbox summary
   - total messages reviewed
   - unread count when available
   - 1-3 sentence overall summary

   ### Priority items
   For each important email include:
   - sender
   - subject
   - why it matters
   - requested action
   - deadline or time sensitivity

   ### Suggested next steps
   - quick bullets for what to do next

5. Draft replies when requested.
   - Keep drafts short, clear, and ready to send.
   - Match the sender's tone when appropriate.
   - If information is missing, leave clear placeholders instead of inventing facts.

## Decision rules
- Prefer concise summaries over long paraphrases.
- Surface risk early: deadlines, money, access, legal/compliance, customer escalations, or executive requests.
- Do not mark newsletters or automated notifications as urgent unless the content clearly requires action.
- When multiple related emails appear, collapse them into one thread-level summary.
- If the user asks what to do first, recommend the smallest high-impact action.

## Output templates

### Template: inbox triage
Use this default format:

## Inbox summary
[short overall summary]

## Priority items
1. **[subject]** — [sender]
   - Why it matters: [reason]
   - Action needed: [action]
   - Timing: [deadline or "no explicit deadline"]

## Other messages
- [short grouped summary]

## Recommended next steps
- [step 1]
- [step 2]

### Template: reply draft
Use this when the user asks for a reply:

Subject: [keep or revise as needed]

Hi [name],

[clear response]

[requested next step or confirmation]

Best,
[sign-off]

## Connector guidance
- When a mail connector is available, search the inbox before answering from memory.
- Read the relevant messages before drafting a reply.
- If the user asks for counts like unread inbox totals, prefer label or folder counts when the mail tool supports them.
- If the request refers to attachments, inspect attachment metadata and read the attachment when possible.

## What not to do
- Do not invent email content, sender intent, or missing context.
- Do not send email automatically unless the user explicitly asks for sending.
- Do not expose raw internal ids or system metadata to the user.
