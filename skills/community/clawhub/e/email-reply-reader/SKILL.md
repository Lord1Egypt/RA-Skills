---
name: email-reply-reader
description: Read and parse job application email replies from companies. Activate when user asks to check job application replies, read recruiter emails, see who responded, check inbox for HR replies, or follow up on job applications. Uses gog Gmail to fetch and classify recruiter responses.
metadata: {"openclaw": {"emoji": "📬", "requires": {"bins": ["gog"]}}}
---

# Email Reply Reader

Reads Gmail inbox, finds job application replies, and classifies each response.

## Prerequisites

`gog` authenticated with Gmail:
```bash
gog auth add you@gmail.com --services gmail
```

## When to Activate

- "查一下有没有回复"、"check my job application replies"
- "有哪些公司回复了"、"did anyone respond to my resume"
- "看看招聘邮件"、"read recruiter emails"

## Workflow

### Step 1: Search for application-related emails

```bash
# Search for replies in the last 30 days
gog gmail messages search "in:inbox (interview OR application OR resume OR opportunity OR position OR role OR job) newer_than:30d" \
  --max 50 \
  --account you@gmail.com \
  --json
```

Also search for sent mail to cross-reference:
```bash
gog gmail messages search "in:sent (application OR resume OR apply) newer_than:30d" \
  --max 50 \
  --account you@gmail.com \
  --json
```

### Step 2: Classify each reply

For each email found, classify it into one of these categories:

| Category | Signals | Next Action |
|---|---|---|
| 🟢 **Interview Invite** | "schedule", "interview", "call", "meet", "availability", "slot" | Reply to confirm ASAP |
| 🔵 **Positive Interest** | "impressed", "interested", "shortlisted", "next steps", "team" | Respond within 24h |
| 🟡 **Request for Info** | "portfolio", "references", "salary", "notice period", "assessment" | Prepare and reply |
| 🟠 **Recruiter Outreach** | "exciting opportunity", "your profile", "perfect fit" (unsolicited) | Evaluate if relevant |
| 🔴 **Rejection** | "unfortunately", "not moving forward", "other candidates", "not a fit" | Log and move on |
| ⚪ **Auto-reply / No Info** | "thank you for applying", "received your application", generic acknowledgement | Wait for real reply |
| ❓ **Unclear** | Hard to classify | Read full email for context |

### Step 3: Output structured summary

Present results in this format:

```
📬 Job Application Replies — Last 30 Days
Found [N] relevant emails from [N] companies

🟢 INTERVIEW INVITES ([N])
━━━━━━━━━━━━━━━━━━━━━━━━
• [Company] — [Role]
  From: [sender name] <email>
  Date: [date]
  Summary: "[key sentence from email]"
  ⚡ Action: Reply to confirm interview slot

🔵 POSITIVE INTEREST ([N])
━━━━━━━━━━━━━━━━━━━━━━━━
• [Company] — [Role]
  From: [sender]
  Date: [date]
  Summary: "[key sentence]"
  ⚡ Action: Respond within 24h

🟡 REQUESTS FOR INFO ([N])
━━━━━━━━━━━━━━━━━━━━━━━━
• [Company] — [Role]
  They need: [portfolio / salary expectations / references]
  ⚡ Action: Prepare and reply

🔴 REJECTIONS ([N])
━━━━━━━━━━━━━━━━━━
• [Company] — [Role] (Date: [date])

⚪ AUTO-REPLIES / PENDING ([N])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• [Company] — applied [date], no human reply yet

────────────────────────────────
⚡ Priority Actions:
1. [Most urgent action]
2. [Second action]
3. [Third action]
```

### Step 4: Offer to draft reply

For interview invites or positive replies, offer to draft a response:

**Interview confirmation template:**
```
Hi [Name],

Thank you for reaching out! I'm very excited about the opportunity to 
interview for the [Job Title] role at [Company].

I'm available at the following times:
- [Option 1: Day, Date, Time + timezone]
- [Option 2: Day, Date, Time + timezone]
- [Option 3: Day, Date, Time + timezone]

Please let me know which works best for your team, or feel free to 
suggest an alternative time if needed.

Looking forward to speaking with you!

Best regards,
[Name]
```

**Rejection acknowledgement (optional — keeps door open):**
```
Hi [Name],

Thank you for letting me know. While I'm disappointed, I appreciate 
you taking the time to follow up.

I remain a big admirer of [Company] and would welcome the opportunity 
to be considered for future roles that may be a better fit.

Best regards,
[Name]
```

## Reading Full Email Content

To read the full body of a specific email:
```bash
# Get thread details (use thread ID from search results)
gog gmail search "from:company.com" --max 5 --account you@gmail.com --json
```

## Follow-up Reminder Logic

For applications with no reply after 7 days, suggest a follow-up:

```
⏰ Follow-up Suggestions (no reply after 7+ days):
• [Company] — applied [N] days ago
  Draft a polite follow-up? [yes/no]
```

**Follow-up template:**
```
Subject: Following Up — Application for [Job Title]

Hi [Name / Hiring Manager],

I wanted to follow up on my application for the [Job Title] position 
submitted on [date]. I remain very interested in this opportunity and 
would love to learn about next steps.

Please let me know if you need any additional information.

Thank you for your time.

Best regards,
[Name]
```
