---
name: email-manager
description: >
  Comprehensive AI email attendant for OpenClaw agents. Use this skill whenever the user asks
  about email, wants to check or sort their inbox, asks about important messages, wants to reply
  to an email, asks what emails need their attention, wants to set up email monitoring, wants to
  manage spam, or mentions anything about organizing their mailbox. Also triggers for scheduling
  email checks, managing email folders, reviewing pending or high-priority messages, or asking
  about the daily email report. This skill assumes an email MCP or equivalent tool is already
  connected to the agent — it does not set one up. Trigger this skill proactively whenever
  email management, inbox organization, or email-related workflows are mentioned.
---

# Email Manager Skill

A complete email attendant for OpenClaw. Organizes inboxes, kills spam, surfaces important emails,
tracks emails awaiting your reply, and keeps a rolling important-message log when phone notifications
are not available. Works with any connected email MCP or tool — the connection method is irrelevant
as long as email list/read/send/move/folder operations are available.

> **Read `references/rules-and-state.md`** before any processing run — it contains your live rule
> sets, folder matrix, approved senders, and notification log. If the file does not yet exist,
> initialize it using the template in that reference file's header.

---

## Folder Structure

Always ensure these folders exist before processing. Create any that are missing (use the `folder`
operation with action `create`). Do NOT create others without user approval (see Folder Management).

| Folder | Purpose |
|---|---|
| INBOX | Unprocessed / new arrivals |
| /1_Important | High-priority emails needing attention |
| /2_WaitingReply | Emails where a response is expected from the user |
| /3_AI_Review | Draft responses awaiting user approval |
| /4_Processed | Handled / archived |
| /Spam | Junk and solicitations |
| *(approved newsletter folders)* | Created per approved sender, named clearly e.g. `/NL_TechCrunch` |

---

## Scheduled Processing (Heartbeat)

OpenClaw schedules email processing via its built-in scheduler/heartbeat. When the user sets or
changes the check interval, **update the scheduled job** — do not just note the preference.

Default schedule: **every 30 minutes** per inbox.

When the user says something like "check email every hour" or "switch to every 15 minutes":
1. Confirm which inboxes are affected (all, or specific address).
2. Update the OpenClaw scheduled job for each affected inbox.
3. Confirm the change back to the user.

Each scheduled run calls the **Full Processing Cycle** below.

---

## Full Processing Cycle

Run this when triggered by the scheduler or when the user asks to "check email", "sort inbox", etc.
Process up to 50 emails per inbox per run. If more remain, the next scheduled run continues.

### Step 1 — Load State
Read `references/rules-and-state.md`. Note:
- Spam sender list
- Approved senders / newsletter list
- Folder routing matrix
- Important email definition
- Sent-history cache (last 90 days of outbound addresses, for solicitor detection)

### Step 2 — List Inbox Emails
Use the email tool `list` operation: type=emails, folder=INBOX, emails=50.

### Step 3 — Classify Each Email

For each email apply these rules **in order** (first match wins):

#### 3a. Spam / Solicitor Detection
Mark as **Spam** if ANY of the following are true:
- Sender is on the spam sender list in state.
- Subject or preview contains classic spam signals (prize/winner/lottery/urgent wire transfer/verify
  your account/click here to claim/limited time offer/you've been selected/unsubscribe-heavy footer
  with no personal content).
- Sender is not in the approved sender list AND the email reads as a cold outreach / solicitation
  (marketing pitch, sales introduction, unsolicited offer, "I came across your profile") AND there
  is **no prior reply thread with this sender** (check sent history before marking — if we have
  replied to this person before they are not a cold solicitor).
- Domain matches a known spam domain in state.

> **Solicitor Rule**: A sender asking for a reply (e.g., "let me know if you're interested") does
> NOT automatically create a WaitingReply item. If the email itself is a solicitation, it goes to
> Spam regardless of how it's phrased.

Move to `/Spam`. Add sender domain to spam list in state (unless it is a major legitimate service
domain like gmail.com, outlook.com — add the full address instead).

#### 3b. Approved Newsletter / Mailing List
If sender is on the approved sender list:
- Route to that sender's designated newsletter folder (e.g., `/NL_TechCrunch`).
- If no folder exists yet for this sender, create one named `/NL_<SenderName>` and update the
  folder routing matrix.
- Move email and continue.

#### 3c. Important Email
Flag as **Important** if ANY of the following are true (baseline — user can extend via rules):
- Subject or body contains urgency language: "urgent", "asap", "time-sensitive", "deadline",
  "action required", "immediately", "expires", "overdue", "past due", "final notice".
- Email is from a known contact (sender appears in sent history as someone we've written to).
- Sender matches any user-defined important-sender rules in state.
- Email is from a financial institution, legal entity, government body, employer, or direct client
  (use judgment based on sender domain and content).

Move to `/1_Important`. Log to notification queue in state (see Notifications).

#### 3d. Needs Reply Detection
An email belongs in `/2_WaitingReply` if ALL of the following are true:
- It is NOT spam or a solicitation.
- The content clearly expects a personal reply: a direct question, a meeting request, a task
  delegated to the user, or a conversational exchange from someone the user knows.
- It has NOT already been replied to (check thread / sent history).
- It is from a human, not an automated system (receipts, shipping notifications, calendar invites
  without a message body, and system alerts are NOT waiting-reply).

Move to `/2_WaitingReply`. Log to notification queue.

#### 3e. Folder Routing
Check the folder routing matrix in state. If the email clearly matches a folder's description,
move it there and mark as processed.

If no folder matches, move to `/4_Processed` for later review.

### Step 4 — Update State
After processing, update `references/rules-and-state.md`:
- Append any new spam addresses/domains.
- Append any new important emails to the notification log (rolling 7-day window — prune older).
- Update the 24-hour activity counters for the daily report.
- Update sent-history cache with any new sent items discovered this run (list sent folder).

### Step 5 — Notify
See Notifications section. If phone/Twilio MCP is available, send alerts. Otherwise log only.

---

## Processed Queue Review

The `/4_Processed` folder holds emails that didn't match any folder. Periodically (or when user
asks), review it:

1. List all emails in `/4_Processed`.
2. Re-check the folder routing matrix — move any that now match a folder.
3. Look for grouping patterns:
   - 5+ emails from the same sender or same company domain → suggest a dedicated folder.
   - 5+ emails with the same subject theme → suggest a topic folder.
   - 5+ emails of the same type (e.g., bank statements, shipping confirmations) → suggest a type folder.
4. Present grouping suggestions to the user with counts and reasoning.
   Example: *"I found 8 emails from Chase Bank. Would you like me to create a `/Bank_Chase` folder for them?"*
5. **Never create a new folder without explicit user approval.**
6. When user approves a folder name (or suggests an alternate), create it and update the folder
   routing matrix in state.

---

## Folder Management Rules

- **Never create a folder without user approval** (exception: approved newsletter folders for
  senders on the approved list — these are auto-created silently).
- Before suggesting a folder, always check the routing matrix — if an existing folder clearly
  covers the email type, use it.
- When a new folder is created, immediately update the folder routing matrix in state with the
  folder name and a one-sentence description.
- When renaming a folder, update all references in the routing matrix.

---

## Sending & Replying to Email

When the user asks to respond to an email:
- If no folder is specified, look first in `/1_Important`, then `/2_WaitingReply`.
- If the user gives a name, subject, or rough description, find the email by scanning those folders.
- Use the user's personality/digital-twin skill if available for drafting tone and voice.
- Present the draft as **Recommended Response** before sending. Show subject and body.
- Ask: *"Want me to adjust anything, or should I send it?"*
- On approval, use the `send` operation with type=respond and the original email ID.
- After sending, move the original email from its current folder to `/4_Processed`.
- Update sent-history cache in state.

When the user asks to write a new email:
- Draft, present, await approval, then send with type=new.

---

## Notifications

Two modes depending on what's available:

### Mode A — Phone/Twilio Available (MCP tool present)
Send WhatsApp/SMS alerts for:
- **Immediate**: Any email moved to `/1_Important` — include sender, subject, one-line summary.
- **Every 6 hours**: If `/2_WaitingReply` has emails, send a digest listing them (sender + subject).
- **Daily (24h)**: Send the Daily Report (see below).

### Mode B — No Phone Capability (default until Twilio MCP is wired in)
Log all notifications to `references/rules-and-state.md` under the notification log section.
The log retains the **last 7 days** of important-email events. Prune older entries each run.

User can ask at any time:
- *"What important emails came in this week?"* → Read log, summarize.
- *"Any emails waiting my reply?"* → List `/2_WaitingReply`.
- *"Show me today's report"* → Show daily report summary from state.

When Twilio/phone MCP becomes available, update the processing cycle to use Mode A automatically.

---

## Daily Report

Generated and stored every 24 hours. Stored in state under `daily_report` section (current day +
previous 6 days retained). Report covers the previous 24-hour window:

```
DATE: [date]
─────────────────────────────────────
Important emails received:     #
Important emails unaddressed:  #
Emails awaiting your reply:    #
Emails processed:              #
Spam filtered:                 #

EMAIL LOG (Important + WaitingReply + Processed, excludes spam):
  TO: [our address]  |  FROM: [sender]  |  SUBJECT: [subject]
  ...
```

If phone is available, send at a consistent daily time (default 7:00 AM user local time — ask user
to confirm timezone on first run). Otherwise store and make available on request.

---

## User Commands & Responses

| User says | Action |
|---|---|
| "Check my email" / "Sort my inbox" | Run Full Processing Cycle |
| "What emails need my attention?" | List `/1_Important` and `/2_WaitingReply` |
| "What's in my important folder?" | List `/1_Important` |
| "What emails am I waiting to reply to?" | List `/2_WaitingReply` |
| "What did I send recently?" | List sent folder, summarize last 10 |
| "Show me today's report" / "Daily report" | Display daily report from state |
| "What important emails came in this week?" | Read notification log from state |
| "Check the processed queue" | Run Processed Queue Review |
| "That email from X is not spam" | Add sender to approved list; move email from Spam back to Inbox; re-classify |
| "Mark X as important" | Add sender/keyword to important rules in state |
| "Approve [newsletter name]" | Add to approved senders; create newsletter folder; route future emails |
| "Check email every [interval]" | Update scheduled job in OpenClaw + confirm |
| "Reply to [description]" | Find email, draft response, present for approval |
| "Write an email to [person] about [topic]" | Draft, present, await approval, send |
| "How many emails are waiting in processed?" | Count `/4_Processed`, summarize grouping opportunities |

---

## Anti-Spam & Approved Sender Management

- Spam additions are **permanent** in state unless user removes them.
- When user says "that's not spam" for a sender: (1) remove from spam list, (2) add to approved
  list, (3) move the email back to Inbox for re-classification, (4) scan Spam folder for other
  emails from same sender and move them too.
- Approved newsletters auto-get a `/NL_` folder. Regular approved contacts just bypass spam
  filtering and route normally.
- Never add a full major provider domain (gmail.com, yahoo.com, outlook.com, icloud.com) to spam.
  Always add the specific address.

---

## First-Run Setup

On first use for a new inbox:
1. Check which standard folders exist; create any missing ones.
2. Initialize `references/rules-and-state.md` from the template.
3. Ask the user:
   - *"What email addresses should I monitor?"*
   - *"How often would you like me to check? (default: every 30 minutes)"*
   - *"Anything specific you always want flagged as important?"*
   - *"Any newsletters or senders you know you want to keep?"*
4. Set up the OpenClaw scheduled job for each inbox at the chosen interval.
5. Run the first Full Processing Cycle.

---

## Reference Files

- **`references/rules-and-state.md`** — Live state: spam list, approved senders, folder routing
  matrix, important-email rules, notification log, daily report history, sent-history cache.
  Read this at the start of every processing run. Write updates at the end of every run.

---

*Keep processing runs focused. Work 50 emails at a time. Be decisive on spam — when in doubt and
there is no prior conversation history with the sender, it's spam. Surface only genuinely important
or actionable emails to the user's attention. The goal is zero inbox, zero noise.*
