---
name: "Arabic Localization Review Skill"
version: 0.1.0
slug: "arabic-localization-review-skill"
description: "Review Arabic and bilingual localization for apps, websites, course notes, and UI screens with RTL, tone, terminology, and consistency checks."
category: "Arabic & Localization"
tags:
  - "arabic"
  - "localization"
  - "rtl"
  - "translation-review"
  - "bilingual"
  - "openclaw"
  - "templates"
generated: "2026-06-13"
---

# Arabic Localization Review Skill

## Purpose

Use this skill to review Arabic and bilingual content before it is shipped, posted, or added to an app. It focuses on meaning, tone, right-to-left readability, UI fit, and EN/AR consistency without rewriting the user's intent.

Good use cases:
- Arabic app screens and onboarding text.
- English-to-Arabic or Arabic-to-English UI copy review.
- Arabic education, language-learning, and explainer content.
- Website sections, landing pages, captions, FAQs, and support text.
- Bilingual templates where English and Arabic must say the same thing.

## Core Safety Rules

1. Do not ask for passwords, OTPs, private account data, customer records, keys, tokens, or confidential documents.
2. Do not invent religious, legal, medical, or financial claims. If wording is sensitive, mark it as "needs human/native review".
3. Preserve the user's intended meaning. Do not silently add promises, guarantees, insults, politics, or claims that were not in the source.
4. Keep cyber/security wording defensive and educational only.
5. If the source text is unclear, list assumptions and ask for the missing context instead of guessing.
6. For public brand content, avoid overclaiming. Use careful words like "helps", "supports", "can reduce risk" instead of guaranteed outcomes.

## Inputs

Ask for only the minimum needed:

- Source text or screenshot text.
- Target audience: Kuwait/GCC, students, customers, internal team, children, etc.
- Desired tone: formal, friendly, educational, marketing, support, or simple Arabic.
- Dialect preference: Modern Standard Arabic, Kuwaiti-friendly wording, Gulf-friendly wording, or bilingual.
- Output length limit if the text must fit a button/card/slide.
- Whether the review should be strict correction only or improved copy.

## Review Workflow

### 1. Meaning Match

Compare source and target:
- Main idea preserved.
- No missing warnings, conditions, numbers, dates, prices, names, or CTA details.
- No extra promises or exaggerated claims.
- Technical terms translated consistently.

### 2. Arabic Quality

Check:
- Grammar and sentence flow.
- Natural phrasing, not literal machine translation.
- Clear subject/verb/object order.
- Good punctuation and Arabic comma/period use where appropriate.
- Avoid awkward mixed English unless the brand style needs it.

### 3. RTL and UI Fit

For apps, slides, and websites:
- Text direction is right-to-left for Arabic blocks.
- Numbers, URLs, emails, and phone numbers remain readable.
- Buttons are short enough.
- Line breaks do not split important phrases badly.
- Icons/arrows/progress direction make sense in RTL layouts.
- Mixed EN/AR text is not visually confusing.

### 4. Tone and Audience

Check whether the Arabic tone fits:
- Formal business Arabic.
- Friendly customer Arabic.
- Simple student/child-friendly Arabic.
- Professional cybersecurity Arabic.
- Marketing copy without sounding spammy.

### 5. Terminology Consistency

Create or update a mini glossary for repeated terms. Example:

| English | Arabic option | Notes |
|---|---|---|
| Cybersecurity | الأمن السيبراني | Preferred formal term |
| Password | كلمة المرور | Use consistently |
| Multi-Factor Authentication | المصادقة متعددة العوامل | Can use MFA in parentheses |
| Phishing | التصيد الاحتيالي | Avoid vague wording |
| Data breach | تسريب بيانات | Use only if breach is confirmed |

### 6. Final Quality Gate

Before final answer, classify the result:
- READY: safe to use with minor/no changes.
- NEEDS EDIT: meaning mostly correct but requires fixes.
- BLOCKED: mismatch, sensitive claim, missing context, or unreadable UI.

## Output Format

Use this structure:

```text
Status: READY / NEEDS EDIT / BLOCKED

Main finding:
- [One short summary]

Fixes:
1. Original: ...
   Suggested: ...
   Why: ...

Consistency notes:
- [Terms, names, CTA, numbers, phone/email/website]

RTL/UI notes:
- [Line breaks, direction, button length, mixed text]

Final Arabic copy:
[copy-ready Arabic text]

Optional English back-translation:
[only when useful]
```

## Copy Review Checklist

Use this checklist for fast reviews:

- [ ] Same meaning as the source.
- [ ] No missing CTA/contact details.
- [ ] No unsupported claims.
- [ ] Arabic reads naturally.
- [ ] Tone fits audience.
- [ ] Technical terms are consistent.
- [ ] RTL layout is readable.
- [ ] Numbers, dates, email, website, and phone are correct.
- [ ] Text fits the UI/slide/card.
- [ ] Sensitive topics marked for human review if needed.

## Example Prompts

### App Screen Review

```text
Review this app screen Arabic localization.
Audience: Kuwait users.
Tone: friendly and clear.
Check meaning, RTL, button length, and terminology.
Source EN: [paste]
Arabic draft: [paste]
```

### Bilingual Carousel Review

```text
Check this English/Arabic carousel pair before posting.
Make sure the Arabic says the same thing as English, contact details match, and the CTA is safe.
Return READY / NEEDS EDIT / BLOCKED.
```

### Arabic Education Content

```text
Review this Arabic lesson text for clarity and age-appropriate wording.
Do not change the learning objective.
Give corrected copy and a short reason for each change.
```

### Website Localization

```text
Review this website section for Arabic localization.
Check headings, button text, SEO-friendly wording, and whether the Arabic sounds natural for GCC customers.
```

## Common Pitfalls

- Translating "security" as a generic safety word when the context is cybersecurity.
- Using too-formal Arabic for simple app onboarding.
- Mixing English acronyms without explanation for beginners.
- Leaving English punctuation order inside Arabic paragraphs.
- Making Arabic text too long for buttons or cards.
- Mirroring all icons automatically: some security icons should stay the same, but arrows/progress indicators may need RTL review.
- Claiming "breach" or "hack" when the source only says "risk" or "alert".

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
