# Email Manager — Rules & State

> This file is read at the start of every processing run and written at the end.
> It is the agent's persistent memory for email management.
> Initialize this file on first run using the sections below.

---

## Monitored Inboxes

```
# Format: email_address | check_interval_minutes | openclaw_job_id
# Example:
# user@example.com | 30 | job_email_001
```

---

## Folder Routing Matrix

> Update this whenever a folder is created or renamed.
> The agent uses this to decide where emails belong during processing.

```
INBOX              | New / unprocessed arrivals — starting point for all email
/1_Important       | High-priority emails: urgent, time-sensitive, from known contacts or key senders
/2_WaitingReply    | Emails where the user owes a personal reply (not automated, not solicitations)
/3_AI_Review       | Draft responses created by agent, pending user approval before sending
/4_Processed       | Fully handled emails — archived
/Spam              | Junk, cold solicitations, marketing, spam
```

*(Add new rows here when new folders are created)*

---

## Spam Sender List

> Individual email addresses or domains to always route to /Spam.
> Never add broad domains like gmail.com or outlook.com — add specific addresses only for those.

```
# Format: address_or_domain | date_added | reason
# Example:
# noreply@sketchy-promo.com | 2024-01-15 | unsolicited marketing
```

---

## Approved Senders & Newsletters

> These bypass spam filtering entirely. Newsletters also get auto-routed to their own folder.

```
# Format: address_or_domain | type (newsletter|contact) | folder (if newsletter) | date_added
# Example:
# newsletters@techcrunch.com | newsletter | /NL_TechCrunch | 2024-01-15
# jane@clientdomain.com      | contact    | —              | 2024-01-15
```

---

## Important Email Rules

> Baseline rules are built into the skill. Add user-defined extensions here.
> Baseline (always active): urgency keywords, known contacts, financial/legal/government senders.

```
# Format: rule_type | value | date_added | notes
# rule_type options: keyword, sender_address, sender_domain, subject_contains
# Example:
# sender_domain | mybank.com       | 2024-01-15 | Always flag bank emails
# keyword       | contract         | 2024-01-15 | Flag anything mentioning contracts
# sender_address| boss@company.com | 2024-01-15 | Always important
```

---

## Sent-History Cache

> Rolling 90-day cache of outbound email addresses. Used to detect prior conversations,
> which prevents flagging past correspondents as solicitors.
> Agent updates this each run by scanning the Sent folder.

```
# Format: sent_to_address | last_sent_date
# Example:
# client@somedomain.com | 2024-03-10
```

---

## Notification Log (Rolling 7-Day Window)

> Important email events are logged here when phone/Twilio is not available.
> Prune entries older than 7 days at the end of each processing run.
> User can ask "what important emails came in this week?" to read this.

```
# Format: timestamp | inbox | event_type (important|waiting_reply) | from | subject | one_line_summary
# Example:
# 2024-03-15T09:22:00 | user@example.com | important | boss@work.com | Q1 Budget Deadline | Asks for budget submission by Friday
```

---

## 24-Hour Activity Counters

> Reset every 24 hours when the daily report is generated.

```
window_start: 
important_received: 0
important_unaddressed: 0
waiting_reply_count: 0
emails_processed: 0
spam_filtered: 0
```

---

## Daily Report History

> Stores last 7 daily reports. Oldest is pruned when 8th is added.

```
# Each report block:
# --- REPORT [date] ---
# (report content)
# --- END REPORT ---
```

---

## Processing Notes

> Scratch space for agent notes during runs — e.g., "Processed 50 of 127 in inbox, 77 remain".
> Overwritten each run.

```
last_run: 
emails_remaining_in_inbox: 0
notes: 
```
