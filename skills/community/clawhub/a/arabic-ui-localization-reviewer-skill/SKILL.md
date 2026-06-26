---
name: "Arabic UI Localization Reviewer Skill"
version: 0.1.0
slug: "arabic-ui-localization-reviewer-skill"
description: "Review Arabic app and website UI localization for RTL layout, translation quality, terminology consistency, tone, and launch readiness."
category: "Arabic & Localization"
tags:
  - "arabic"
  - "localization"
  - "rtl"
  - "ui-review"
  - "templates"
generated: "2026-06-08"
---

# Arabic UI Localization Reviewer Skill

## Purpose

Use this skill to review Arabic localization for websites, mobile apps, landing pages, dashboards, forms, and onboarding screens. It helps an assistant check whether Arabic UI copy is natural, readable, culturally appropriate, and technically ready for right-to-left layouts.

The skill is for review, drafting, and QA guidance only. It does not publish changes, collect credentials, or modify production systems unless the user explicitly approves a separate implementation step.

## When to use

Use this skill when the user asks to:

- Review Arabic app or website text.
- Convert English UI copy into Arabic UI copy.
- Check RTL layout problems in screenshots.
- Compare Arabic and English screens for missing meaning.
- Improve Arabic button labels, error messages, headings, onboarding text, or help text.
- Prepare a localization QA checklist before launch.
- Make Arabic text sound natural, professional, and user-friendly.

## Inputs to request

Ask for only the inputs needed for the review:

1. The product type: website, app, dashboard, form, email, landing page, or other.
2. The audience: Kuwait, GCC, general Arabic speakers, students, business users, parents, gamers, etc.
3. The tone: formal, friendly, simple, premium, government-style, youth-style, or educational.
4. The English source text, Arabic draft, screenshots, or screen list.
5. Any fixed terminology or brand words that must not change.
6. Target dialect preference if needed: Modern Standard Arabic by default; Gulf/Kuwaiti flavor only if requested.

Do not ask for passwords, OTP codes, private account data, API keys, or customer records.

## Review checklist

### 1. Meaning and completeness

- Confirm the Arabic text preserves the same meaning as the source.
- Flag missing warnings, conditions, prices, dates, limits, or legal/safety notes.
- Identify mistranslations, literal translation, or awkward phrases.
- Check that buttons and labels describe the actual action.

### 2. Arabic quality

- Prefer clear Modern Standard Arabic unless the user requests dialect.
- Keep UI copy short and scannable.
- Avoid overly formal or machine-like wording.
- Fix grammar, word order, punctuation, and readability.
- Keep repeated terms consistent across screens.

### 3. RTL layout and visual QA

When screenshots are provided, check:

- Text direction is right-to-left.
- Numbers, English words, brand names, email addresses, and URLs display correctly.
- Icons point in the correct direction.
- Back/next arrows are mirrored only where appropriate.
- Text is not clipped, overlapped, or too small.
- Buttons have enough padding for Arabic expansion.
- Fields, labels, and validation messages align cleanly.
- Mixed Arabic/English lines do not break awkwardly.

### 4. UX clarity

- Replace vague labels with action-focused labels.
- Make error messages explain what happened and how to fix it.
- Make empty states helpful.
- Make confirmation messages clear and reassuring.
- Make destructive actions clearly labeled and reversible when possible.

### 5. Cultural and regional fit

- Avoid idioms that may not work across Arabic audiences.
- Use respectful wording for sensitive topics.
- Use Kuwait/GCC terms only when appropriate.
- Avoid unsupported claims, exaggerated promises, or pressure language.

### 6. Launch readiness

Before launch, recommend checking:

- Every screen has Arabic text.
- No placeholder text remains.
- Date, time, currency, address, and phone formats are suitable for the target region.
- Legal, privacy, payment, and support text was reviewed by the responsible owner.
- Arabic and English versions match in functionality and important meaning.

## Output format

Return a concise review in this structure:

```text
Arabic Localization Review

Status: Ready / Needs small fixes / Needs major fixes
Audience: [target audience]
Tone: [tone used]

Top issues:
1. [issue] -> [why it matters] -> [suggested fix]
2. [issue] -> [why it matters] -> [suggested fix]
3. [issue] -> [why it matters] -> [suggested fix]

Suggested Arabic copy:
- Screen/field: [name]
  Current: [current text]
  Better: [improved text]

RTL/layout notes:
- [visual/layout issue or "No major RTL layout issue seen"]

Next step:
- [one practical action]
```

## Rewrite template

Use this when the user wants improved Arabic copy:

```text
Goal: Make the UI copy clear, natural, and short.
Tone: [formal/friendly/simple]
Audience: [target]

Original English:
[paste]

Current Arabic:
[paste if available]

Improved Arabic:
[copy]

Why this is better:
- [short reason]
```

## Screenshot QA template

Use this when the user provides screenshots:

```text
Screenshot QA

Screen: [name]
Status: Pass / Fix needed

Text readability:
- [notes]

RTL/layout:
- [notes]

Copy quality:
- [notes]

Priority fixes:
1. [fix]
2. [fix]
3. [fix]
```

## Safety rules

- Do not request secrets, OTPs, passwords, session cookies, private customer data, or internal credentials.
- Do not claim legal, religious, medical, or financial approval; only provide wording suggestions.
- Do not publish or change production copy without explicit user approval.
- Do not invent brand policies or official terms. Ask for the user's glossary when needed.
- If screenshots include private data, tell the user to blur or remove it before sharing.

## Good defaults

- Default Arabic style: clear Modern Standard Arabic.
- Default review depth: practical UI/UX QA, not academic translation theory.
- Default output length: short and actionable.
- Default recommendation: fix high-impact meaning, CTA, and layout issues first.

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
