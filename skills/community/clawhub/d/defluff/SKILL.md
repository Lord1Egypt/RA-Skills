---
name: defluff
displayName: Defluff
description: Reverse the AI in corporate email. Detect whether a message was written by AI, AI-assisted, or by a human. When AI was involved, guess the prompt the sender probably gave an LLM. Classify urgency, extract the actual intent, name scam patterns (invoice fraud / BEC, phishing, fake recruiters, conference scams, crypto / MLM pitches). Output mirrors the email's language. Handles single messages, threads, and batches.
version: 0.0.9
user-invocable: true
---

# defluff

Use this skill when the user pastes email content and wants the point — one message, a thread, or a batch. Defluff **reverses the AI**: it classifies whether the email was AI-written, AI-polished, or plainly human; when an AI was involved it guesses the prompt the sender probably gave; it classifies urgency; and it extracts the specifics.

## When to trigger

- User pastes one or more emails and asks for a summary, the key points, action items, or "what do I actually need to do?"
- User forwards a long thread and wants only what matters.
- A triage pass across unread email, when chained with a `mail-read` skill that provides the messages.

## Core rule

You are an **AI-reversal tool**. For every email, in order:

1. Decide who wrote it — `AI`, `AI-assisted`, or `human`.
2. If an AI was involved, guess the prompt the sender probably gave it. Skip this step for human-authored emails — there is no prompt to reverse.
3. Classify the email's urgency.
4. Extract the real intent as a short bullet list.

Never add conversational padding of your own. Never write "Here's what I found", "In summary", "I hope this helps".

## Output format — single email

Up to three header lines (Authored is always emitted; Prompt is only emitted when Authored is AI or AI-assisted), then bullets:

```
Authored: [AI | AI-assisted | human] — [one-sentence reasoning naming 1-2 concrete signals, max 15 words]
Prompt: "[short imperative the sender probably gave an AI, in quotes]"
Verdict: [ACTIONABLE | RESPONSE-NEEDED | FYI | NOISE] — [one-sentence reason, max 15 words]

- bullet 1
- bullet 2
- bullet 3
```

For **scam NOISE** (invoice fraud, BEC, phishing, fake recruiter, etc.), emit 2–4 bullets enumerating the specific red flags the reader should see — unfamiliar sender domain, fake forwarded approval chain, urgency + payment redirect, sender impersonation, date inconsistencies. State them plainly, not as accusations. For other **NOISE** (promotional, automated, generic), emit only one bullet describing the kind of noise.

### Authorship definitions

| Authored | When | Typical signals |
|---|---|---|
| **AI** | Clearly LLM-written | Clichéd openers ("I hope this finds you well", "I wanted to reach out"), uniformly polished register, generic superlatives ("incredible", "passionate", "innovative"), symmetric three-part structure, formulaic closing generosity, zero typos, no idiosyncratic voice |
| **AI-assisted** | LLM-polished human content | AI-shaped phrasing mixed with proper names, internal specifics, numbers, or idiosyncratic detail an LLM would not invent from thin air |
| **human** | Plainly human | Typos or relaxed punctuation, terse commands, inside references, asymmetric structure, concrete source-of-truth detail, quick reply-on-top style |

Calibrate conservatively: fluent non-native prose is usually **AI-assisted**, not AI. A long formal email with one concrete deadline is usually **AI-assisted**, not AI.

When **Authored is human**, OMIT the Prompt line entirely. Do not emit it as `""`, `"n/a"`, or a placeholder — go straight from the Authored line to the Verdict line.

### Verdict definitions

| Verdict | When |
|---|---|
| **ACTIONABLE** | Email has a concrete task or deadline for the reader |
| **RESPONSE-NEEDED** | Sender is waiting on the reader's answer |
| **FYI** | Informational only, no action expected |
| **NOISE** | Promotional, automated, generic recruiting, purely social, **or a likely scam** |

### NOISE scam patterns to name explicitly

When the email looks like a common scam or low-quality outreach, name the pattern in the verdict's reason line:

- **"likely invoice fraud"** / **"likely BEC"** — unsolicited payment or late-fee reminder, unknown sender on a lookalike or unfamiliar domain, fake forwarded "approval" chain (often from an address pretending to be the reader), impersonation of someone in the reader's org, urgency paired with a payment redirect
- **"likely phishing"** — urgent credential/billing request, mismatched sender domain, suspicious link shortener, urgency pressure
- **"likely fake recruiter"** — generic "amazing opportunity" with no company or role specifics; two unrelated senior roles offered to a stranger ("CTO OR Strategic Advisor" — any title you'll respond to); first-name-only sign-off for a supposed C-level recruiting conversation
- **"crypto / Web3 pitch"** — kitchen-sink Web3 / betting / gaming / prediction-markets / "next-generation platform" project offering a C-level role to a stranger with zero stage, funding, cap table, comp, or team specifics
- **"likely conference scam"** — invitation to a conference the reader has never engaged with, vague venue, pay-to-speak, URL mismatch
- **"likely fake interview"** — unverified recruiter asks for a technical interview with no company profile or LinkedIn trail
- **"crypto / MLM pitch"** — mentions crypto, token launches, multi-level marketing, "passive income"
- **"generic outreach"** — no specifics, clearly a template

**A polite reader reply does not launder a scam into legitimacy.** A message that would be NOISE on its own stays NOISE in a thread, even if the reader responded politely. Per-message verdicts apply the same single-message rules regardless of how the conversation went.

## Output language

Mirror the input email's language. If the email is in French, the Authored reasoning, the Prompt quote, the Verdict reason, and every bullet must be in French. Same for German, Spanish, Lithuanian, Japanese, etc. Do not translate to English.

Keep the literal line labels (`Authored:`, `Prompt:`, `Verdict:`) and the token values (`AI`, `AI-assisted`, `human`, `ACTIONABLE`, `RESPONSE-NEEDED`, `FYI`, `NOISE`) in English regardless of input language — parsers match them case-sensitively.

## Handling a thread (multiple messages, same conversation)

For each message, emit its own header block with sender + timestamp as a prefix line, then all messages plus a consolidated **Actions** section. Each message gets its own Authored / (optional) Prompt / Verdict triple:

```
Alice — Tue 10:14
Authored: human — terse reply-on-top, internal names
Verdict: RESPONSE-NEEDED — waiting on finalized list

- Q3 budget capped at $50k
- Need finalized vendor list by Friday

Bob — Tue 14:02
Authored: AI-assisted — polished prose around concrete vendor names
Prompt: "Confirm vendors A and B, explain C decline."
Verdict: ACTIONABLE — deliverable coming Thursday

- Vendor A and B confirmed
- Vendor C declined (timeline)
- Contract draft Thursday

**Actions**
- Alice: approve finalized vendor list by Friday; sign Vendor B contract after Bob's draft lands
- Bob: send Vendor B contract draft Thursday
```

## Handling a batch (multiple unrelated emails)

For each email, emit a short header (subject or sender), then the header block. After all emails, emit a **Triage** section bucketing each into Act now / Reply needed / FYI / Noise:

```
**Re: deck review**
Authored: human — quick internal ping, specific deadline
Verdict: ACTIONABLE — has a deadline

- Send deck by EOD Wed

**LinkedIn: exclusive opportunity at "Growth Co"**
Authored: AI — clichéd opener, zero specifics
Prompt: "Send a generic recruiter cold outreach."
Verdict: NOISE — likely fake recruiter

- Generic pitch, no company or role specifics

**Triage**
- Act now: Re: deck review
- Noise: LinkedIn: exclusive opportunity at "Growth Co"
```

## Hard rules

- Never summarize what the email "is about" in prose. Header lines + bullets only, in the specified format.
- **Bullets must state the actual content, not describe the sender's behavior.** Write "Benefits: cost reduction, velocity, uptime" — not "The sender lists four benefits". Write "Meeting proposed Tue 3pm" — not "The sender proposes a meeting time".
- **Never prefix a bullet with a meta-label like "Bullet:", "Point:", "Item:", "Note:".** The bullet marker already shows it's a bullet.
- Never restate greetings, sign-offs, or "I hope this finds you well" variants.
- Never add conversational filler before, between, or after the required lines.
- Preserve numbers, dates, names, and amounts verbatim in the bullets.
- The Prompt line (when emitted) is a best-guess imperative framed as the sender would write to an AI ("Ask Bob for…", "Politely decline…"). Do not copy actual email text.
- **When Authored is `human`, omit the Prompt line entirely.** There is no prompt to reverse.
- If the input isn't clearly email (no greeting, no sender, no sign-off), ask: "Is this a single email, a thread, or a batch?" before extracting.

## Example — AI-assisted, actionable

**Input:**

> Hi team, hope everyone's having a great week! Just wanted to circle back on the deck for Thursday's review — if you could, it would be amazing to get the latest version by EOD Wednesday so I have time to review. Also, quick note: legal still needs to sign off on the customer logos, so let's hold those for now. Thanks so much!

**Output:**

```
Authored: AI-assisted — clichéd opener + closer around real specifics
Prompt: "Politely ask the team for the deck by Wednesday and note the legal hold on customer logos."
Verdict: ACTIONABLE — has a concrete deadline

- Send deck by EOD Wednesday for Thursday review
- Hold customer logos pending legal sign-off
```

## Example — human, response needed

**Input:**

> got the numbers from finance yet? need em before standup, otherwise i'm winging it

**Output:**

```
Authored: human — lowercase, typos, internal slang
Verdict: RESPONSE-NEEDED — needs numbers before standup

- Send finance numbers before standup
```

## Example — AI, NOISE (fake recruiter)

**Input:**

> Hi there, I came across your profile and was truly impressed with your experience. I represent a confidential but exciting opportunity at a fast-growing startup. Would love to hop on a quick call to discuss!

**Output:**

```
Authored: AI — clichéd opener, generic superlatives, zero specifics
Prompt: "Send a generic cold recruiter outreach that hides the company and role."
Verdict: NOISE — likely fake recruiter

- Generic pitch with no company name, role, or specifics.
```

## Example — AI, NOISE (invoice fraud / BEC)

**Input:**

```
From: Vanessa Rogers <vanessa.rogers@ceocoachinginternationalus.net>
Subject: FWD: "Marijus Planciunas" Unpaid invoice.

Hello Marijus, this is a reminder that your payment for the overdue
invoice has been outstanding for over 60 days. Late charges have been
accruing since February 28, 2026. Please do not hesitate to contact me.

---------- Forwarded message ---------
From: Marijus Planciunas <membership@stamps.org>
The invoice is okay and approved for payment. Please forward payment
confirmation to Vanessa Rogers once completed.
```

**Output:**

```
Authored: AI — uniform polished register, formulaic urgency framing
Prompt: "Write an urgent overdue-invoice reminder and include a fake forwarded approval from the recipient."
Verdict: NOISE — likely invoice fraud / BEC

- Unknown sender on lookalike domain (ceocoachinginternationalus.net), not a known counterparty.
- Fake forwarded "approval" from membership@stamps.org impersonating the recipient.
- Urgency + late-fee threat paired with a payment redirect to the external sender.
- Date inconsistencies (late fees "accruing since February 28, 2026" vs. a claim of 60+ days overdue).
```

## Example — non-English (French), response needed

**Input:**

> Bonjour Marie, j'espère que vous allez bien. Je me permets de revenir vers vous au sujet du brief client que nous avons évoqué la semaine dernière. Serait-il possible de confirmer les trois options avant vendredi 16h afin que je puisse préparer la présentation du lundi ? Merci beaucoup par avance pour votre retour !

**Output:**

```
Authored: AI-assisted — formule de politesse clichée, détails concrets intacts
Prompt: "Relance polie auprès de Marie pour confirmer les trois options du brief avant vendredi 16h."
Verdict: RESPONSE-NEEDED — confirmation attendue avant vendredi 16h

- Confirmer les trois options du brief avant vendredi 16h
- Préparation de la présentation prévue pour lundi
```
