---
name: email-triage-pro
description: "Intelligently categorize, prioritize, and draft replies for emails. Fetches emails via web_fetch (Gmail web) or browser, no OAuth required. AI-powered classification into urgent/important/newsletter/spam, generates contextual reply drafts. Use when: (1) user wants email help or inbox management, (2) check inbox, triage emails, find unread messages, (3) draft email replies, (4) find unanswered emails, (5) 'check my email', 'any urgent emails', 'draft a reply', 'email summary'. Homepage: https://clawhub.ai/skills/email-triage-pro"
---

# Email Triage Pro v2.0

**Install:** `clawhub install email-triage-pro`

Email triage and reply drafting. No OAuth or external dependencies — uses web_fetch or browser.

## Language

Detect from user's message language. Default: English.

## How It Works

### Step 1: Fetch Emails

Use the agent's built-in tools. Pick the best available method:

**Method A: web_fetch (Gmail)**
```
web_fetch https://mail.google.com/mail/u/0/#inbox
```
Note: Gmail requires login cookies. If web_fetch returns a login page, fall back to Method B.

**Method B: Browser automation**
```
browser open → https://mail.google.com/mail/u/0/#inbox
browser snapshot → extract email list
```

**Method C: Any webmail**
Works with Outlook.com, Yahoo, etc. — navigate to inbox, snapshot, extract.

If no method works, tell the user:
```
Could not access email. Options:
1. Open your email in the browser and I can read it via screen snapshot
2. Copy-paste email content and I'll categorize + draft replies
3. Set up a Gmail API key for direct access
```

### Step 2: Categorize

Read each email's subject, sender, and snippet. Categorize:

| Category | Criteria | Action |
|----------|----------|--------|
| 🔴 Urgent | Time-sensitive, from boss/client, "ASAP" | Flag immediately |
| 🟡 Important | Work-related, requires response | Draft reply |
| 🟢 Newsletter | Mass email, marketing | Archive suggestion |
| ⚪ Spam/Low | Promotions, automated | Archive suggestion |

### Step 3: Draft Replies

For urgent and important emails only. Rules:
- Match sender's tone
- Max 3 paragraphs
- End with clear next step
- Match sender's language
- Do NOT send — present draft for review

Format:
```
📧 Reply to: {sender} - "{subject}"

---
{draft text}

---
[Reply] [Edit] [Skip]
```

### Step 4: Summary

```
Email Triage ({N} emails):
  🔴 Urgent: {count}
  🟡 Important: {count}
  🟢 Newsletter: {count}
  ⚪ Spam/Low: {count}
  Drafts: {count} ready for review
```

## Quick Commands

| User says | Action |
|-----------|--------|
| "check email" / "sjekk mail" | Fetch + categorize + summarize |
| "check urgent" | Filter urgent only |
| "draft reply to [sender]" | Draft for specific email |
| "email summary" | Summary of recent emails |
| "follow up" | Check for unanswered important emails |

## Paste Mode

If the user pastes email content directly:
1. Categorize immediately
2. Draft reply
3. No fetch needed

## Guidelines for Agent

1. **Use built-in tools first** — web_fetch, then browser, then ask user
2. **Never require OAuth** — always have a fallback
3. **Don't auto-send** — drafts are for review only
4. **Match language** — reply in the email's language
5. **Be concise** — categorize fast, draft short
6. **Track unanswered** — flag emails awaiting reply

## What This Skill Does NOT Do

- Does NOT require OAuth, API keys, or external skills
- Does NOT send emails automatically
- Does NOT store credentials
- Does NOT modify any local files

## More by TommoT2

- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **context-brief** — Persistent context survival across sessions
- **cross-check** — Auto-detect and verify assumptions in your responses

Install the full suite:
```bash
clawhub install setup-doctor context-brief cross-check email-triage-pro
```
