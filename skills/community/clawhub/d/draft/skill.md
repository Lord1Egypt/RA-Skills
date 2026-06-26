---
name: draft
description: >
  Professional first-draft generator. Trigger whenever the user needs to write anything from scratch:
  emails, reports, articles, proposals, memos, cover letters, blog posts, scripts, READMEs, pitch
  decks, social posts, or any other document. Also triggers on phrases like "help me write",
  "I need to send", "write something for", "I don't know how to start", or when the user pastes
  rough notes and needs them turned into a real document.
---

# Draft — First Draft Generator

## What This Skill Does

Eliminates the blank page. Takes any input — a topic, bullet points, a messy brain dump, a one-line
description — and produces a complete, polished first draft ready for immediate use or light editing.

## Core Principle

A good first draft is not a perfect document. It is a complete document. It gives the user something
real to react to, edit, and send — instead of a cursor blinking on an empty page.

## Workflow

### Step 1: Classify the Request
```
DOCUMENT_TYPES = {
  "email":        { structure: ["subject","greeting","context","ask","next_step","sign_off"], length: "50-300 words" },
  "report":       { structure: ["exec_summary","background","findings","analysis","recommendations"], length: "500-2000 words" },
  "article":      { structure: ["hook","context","body","conclusion","cta"], length: "600-1500 words" },
  "proposal":     { structure: ["problem","solution","methodology","timeline","investment","next_steps"], length: "400-1200 words" },
  "memo":         { structure: ["to/from/date/re","purpose","background","action"], length: "150-400 words" },
  "cover_letter": { structure: ["hook","why_them","why_me","evidence","ask"], length: "250-400 words" },
  "readme":       { structure: ["title","description","install","usage","examples","contributing"], length: "300-800 words" },
  "social_post":  { structure: ["hook","value","cta"], length: "50-500 words depending on platform" }
}
```

If document type is ambiguous, infer from context. Only ask if it materially changes the output.

### Step 2: Extract the Brief
```
brief = {
  document_type:  classify(user_input),
  purpose:        what_should_this_accomplish(),
  audience:       who_will_read_this(),
  key_points:     what_must_be_included(),
  tone:           formal | professional | conversational | urgent | warm | bold,
  length:         short | medium | long,
  constraints:    deadlines, word_limits, sensitive_topics
}
```

Inference rules:
- Casual writing → conversational tone
- Mentions company or client → professional tone
- Says "quick" or "short" → brevity is priority
- Pastes bullet points → those ARE the key points, preserve all of them
- No audience specified → infer from document type

### Step 3: Write the Draft

Universal writing rules:
- First sentence must earn attention or clearly state purpose
- Every paragraph has one job — cut sentences that do not serve it
- Active voice. Specific nouns. Strong verbs.
- End with clarity: what happens next, what is being asked, what the reader should feel

Anti-patterns to eliminate:
- "I hope this email finds you well" → delete
- "In today's fast-paced world" → delete
- "As per my previous email" → rewrite as "Following up on [specific thing]"
- Paragraphs longer than 5 lines in emails
- Burying the ask in paragraph 3

### Step 4: Deliver and Offer Adjustments

Present the complete draft. Then offer exactly three targeted options:
```
Draft complete. Options if you want to refine:
1. [Specific tone adjustment relevant to this draft]
2. [Specific length adjustment relevant to this draft]
3. [Specific content addition relevant to this draft]

Or tell me what to change and I will revise immediately.
```

## Format Rules by Document Type

- Emails: plain text with Subject line labeled. No markdown inside the body.
- Reports/Articles: markdown headers. Output ready to paste into a doc.
- READMEs: full markdown with code blocks.
- Social posts: output in a code block for easy copying. Include character count for Twitter/X.
- Proposals: structured sections with headers. Numbers for timelines and pricing wherever possible.

## Tone Calibration
```
TONE_GUIDE = {
  "formal":            "No contractions. Full sentences. Titles used.",
  "professional":      "Contractions OK. Direct. Clear. Respectful but not stiff.",
  "professional-warm": "Professional baseline plus genuine warmth. Human, not corporate.",
  "conversational":    "Write like a smart person talking. Short sentences. Real words.",
  "urgent":            "Lead with the urgency. Short paragraphs. Clear ask. No preamble.",
  "bold":              "Strong opinions. Active voice. No hedging. Confident assertions."
}
```

## Quality Check Before Delivering

- [ ] First sentence is strong — not a throat-clear
- [ ] Every required piece of information from the brief is included
- [ ] No placeholder text remaining
- [ ] Tone matches the request and audience
- [ ] Length is appropriate for document type
- [ ] The ask or purpose is unmistakably clear
- [ ] Draft is complete — not an outline, not bullets, a real document
