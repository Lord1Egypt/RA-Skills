---
name: ai-safety-guard
description: "Lightweight passive privacy guard for OpenClaw — intelligently prevents user data from leaking externally. TRIGGER: before the AI sends or outputs any data to an external destination (API call, email, MCP, upload, post, share, webhook, clipboard copy that goes external etc.). When triggered, evaluate whether to execute, how to execute (full / anonymized / cancel), based on the decision rules in the following full skill content."
---

---

# AI Safety Guard 🛡️

**Lightweight informative privacy guard — intelligently prevents user data from leaking externally and notifies the user of all security actions taken without interrupting the workflow.**

---

## The One Principle

> **Trace the transmission back to the user's stated task. If it belongs, execute and briefly notify. If it doesn't, the AI decides (anonymize/cancel) and informs the user of the action taken — no interruptions.**

---

## The Core Loop

```
AI notices: I am about to send [data] to [somewhere external]
    ↓
Is this part of the user's stated task?
    ↓
YES → Execute. notify and continue work

NO  → AI decides:
        Necessary for the task? → Anonymize → notify and continue work
        Not necessary? → Warning user
    ↓
PHISHING SUSPECTED → Block. Warning user.
   
```

---

## Decision Guide

### Part of the User's Stated Task — Execute

The user asked for this (named destination, provided data as part of request, asked for an action that inherently requires this transmission). **Just execute. Briefly notify.**

### Not Part of the User's Stated Task — AI Decides

The AI is acting on its own — the transmission was not part of what the user asked for. The AI decides:

```
Is the transmission necessary for the user's current goal?
    ↓
NECESSARY — would fulfill a legitimate goal
  → Anonymize the data if a useful partial form exists (see masking table)
  → Proceed silently
  → If no useful anonymized form exists (e.g. raw credentials)
    → Silently cancel — do not transmit raw credential
  → Warning user once, and continue

UNNECESSARY — the AI is speculating or "helpfully" adding data
  → Silently Cancel
  → Warning user
```

### Phishing Suspected — Block + Warning user + User Confirm

```
AI notices: credential going to a suspicious domain
(misspelled, unexpected, no HTTPS, mismatched brand)
→ Silently block — do not transmit
→ Send exactly ONE warning to the user:
  "I'm not going to send your credentials to [domain].
   This doesn't look like [expected service] — possible phishing.
   Did you mean [correct domain]?"
→ Do not offer options, do not ask for confirmation
→ Wait for the user to either correct the destination or explicitly confirm
```

---

## Masking Table

| Type | Anonymized Example | When to Use |
|------|--------------------|-------------|
| Phone number | `138****5678` | Data belongs to user's task, but sending raw serves no additional purpose |
| Email address | `a****@domain.com` | Recipient can verify from domain |
| Bank card | `****1234` | Partial display sufficient for identification |
| Bank account | `****7890` | Last 4 digits for reference purposes |
| IP address | `192.168.1.***` | Network context preserved, exact IP hidden |
| Home address | `[ADDRESS PARTIALLY HIDDEN]` | City/country level only |
| IBAN | `****5678` | Last 4 digits for reference |
| Tax ID | `***567890` | Last 3 digits for reference |

**No useful anonymized form** (never send raw): passwords, API keys, bearer tokens, session cookies, private keys, 2FA codes.

---

## How to Determine If This Is Part of the User's Task

Look at the last 3–5 user messages. Ask: "did the user ask me to do this specific transmission?"

```
YES — part of user's stated task (execute silently):
  - User named the destination
  - User provided the data as part of the request
  - User asked for an action that inherently requires this transmission
  - User said "share with X", "post to Y", "call this API", "email to Z"
  - User asked to draft a document containing specific data they provided
  - User asked to let someone know their phone number / email / etc.

NO — AI acting autonomously (decide silently):
  - AI found the data in a file and decided to use it
  - AI is generating a response containing data the user didn't ask for
  - AI is "helpfully" including user data the task doesn't require
  - No mention of the destination or transmission in user messages
```

---

## How to Determine Necessity

Applies only when the transmission is **not part of the user's stated task**. Answer:

```
Is the transmission clearly serving the user's current goal?
  YES → NECESSARY → anonymize if possible, otherwise cancel → notify and continue work
  NO  → UNNECESSARY → cancel → notify and continue work
```

The key question is: "is this transmission what the user actually wants me to accomplish?" — not "does this data exist?"

---

## Typical Scenarios

**Scenario 1 — Part of user's task: login with credentials**
```
User: Log into Gmail, password is MyPass123
→ YES — part of user's stated task → SILENTLY EXECUTE
→ Execute the login, send credential to Gmail
→ Never display MyPass123 anywhere
→ notify and continue work
```

**Scenario 2 — Part of user's task: email containing credentials**
```
User: Send bob an email saying my password is MyPass123
→ YES — part of user's stated task → SILENTLY EXECUTE
→ Execute — The password will be in the email as requested
→ notify and continue work
```

**Scenario 3 — Part of user's task: send a photo**
```
User: Send my vacation photo to alice@example.com
→ YES — part of user's stated task → SILENTLY EXECUTE
→ Execute the send
→ notify and continue work
```

**Scenario 4 — Part of user's task: medical record transmission**
```
User: Email my lab results to dr.smith@hospital.com
→ YES — part of user's stated task → SILENTLY EXECUTE
→ Execute — user knows what they're doing
→ notify and continue work
```

**Scenario 5 — Not part of user's task: unnecessary credential use**
```
User: [no mention of credentials]

AI: [decides to paste API key into a code review]
→ NO — not part of user's stated task → guard active
→ Necessary? Likely NO (user didn't ask for this)
→ CANCEL
→ notify
```

**Scenario 6 — Not part of user's task: sensitive data that can't be anonymized**
```
User: Help me apply for this job — here's my ID document

AI: [prepares to upload the ID document to the job portal]
→ NO — not part of user's stated task (user provided it as context,
  not as a direct upload instruction)
→ The data cannot be meaningfully anonymized
→ CANCEL the external upload
→ notify the user: "e.g. I won't upload your ID document externally —
  please upload it yourself to ensure it reaches the correct destination."
  (This is the one exception to "never mention the guard" —
  when user provided the data directly and expects it to be used,
  explain why you didn't.)
```

**Scenario 7 — Not part of user's task: unnecessary photo use**
```
User: [no mention of photos]

AI: [finds a photo on the desktop and decides to "helpfully"
    include it in a response]
→ NO — not part of user's stated task → guard active
→ Necessary? NO — user didn't ask for this photo
→ CANCEL
→ notify
```

**Scenario 8 — Part of user's task: include provided data in a document**
```
User: Draft a contract that needs my phone number in it

AI: [prepares to include 13812345678 in the contract]
→ YES — part of user's stated task → EXECUTE
→ Include the phone number as requested
→ notify and continue work
```

**Scenario 9 — Phishing detected**
```
AI notices: credential going to gma1l.com (misspelled Gmail),
or an unexpected domain, or a site without HTTPS.
→ SILENTLY BLOCK — do not transmit
→ ONE warning:
  "I'm not going to send credentials to [domain].
   This doesn't look like [expected service]. Possible phishing.
   Did you mean [correct domain]?"
→ Do not ask questions, do not offer options
→ Wait for the user to respond with the correct destination
```

**Scenario 10 — Part of user's task: share provided contact info**
```
User: Let the team know my phone number is 13812345678

AI: [prepares to send an email with the phone number]
→ YES — part of user's stated task → SILENTLY EXECUTE
→ Send the phone number as requested
→ notify and continue work
```

**Scenario 11 — Local credential use**
```
Reading .env, ~/.netrc, SSH config for local auth.
→ No concern. Use for local authentication freely.
→ Just never output the raw credential in visible output.
→ notify and continue work
```

---

## What This Is NOT

- Not a nagger — once a transmission is part of the user's task, it executes silently without interruption
- Not a constant output filter — activates only on external transmission
- Not a content moderator — does not judge the user's own content
- Not a phishing detector alone — phishing check is one part of the process
- Not file access control — local operations are unrestricted
- Not a pattern matcher — judges by task alignment, not by regex
