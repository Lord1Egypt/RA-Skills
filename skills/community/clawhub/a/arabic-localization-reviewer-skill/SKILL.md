---
name: "Arabic Localization Reviewer Skill"
version: 0.1.0
slug: "arabic-localization-reviewer-skill"
description: "Review Arabic localization, RTL layout, bilingual wording, tone, and translation quality with clear safety and quality gates."
category: "Arabic & Localization"
tags:
  - "arabic"
  - "localization"
  - "rtl"
  - "translation-review"
  - "bilingual"
  - "openclaw"
  - "templates"
generated: "2026-06-12"
---

# Arabic Localization Reviewer Skill

## Purpose

Use this skill to review Arabic or bilingual Arabic/English content before it is published, shipped, or shared with learners, customers, users, or the public.

It helps check:
- Meaning accuracy between source and Arabic text.
- Natural tone for the target audience.
- RTL layout and punctuation issues.
- UI label clarity and length.
- Mixed Arabic/English formatting.
- Cultural sensitivity and professional wording.
- Final publish-readiness without exposing private data.

## When to use

Use this skill when the user asks to:
- Review Arabic translation quality.
- Localize English UI, captions, lessons, app screens, or website copy into Arabic.
- Check bilingual Arabic/English content for tone and meaning.
- Audit RTL layout problems in a screenshot, app, design, slide, or document.
- Improve Arabic wording for education, business, cybersecurity awareness, family apps, or social posts.
- Prepare a localization QA checklist before release.

## Required inputs

Ask for only what is needed:
1. Source text or screenshot.
2. Arabic draft if available.
3. Target audience, for example children, parents, students, clients, or general public.
4. Tone preference, for example formal, friendly, educational, marketing, or simple.
5. Country or dialect preference if relevant.
6. Output format: quick notes, revised copy, QA table, or release checklist.

Do not ask for passwords, tokens, private account details, user databases, or confidential client material.

## Review workflow

### 1. Identify the content type

Classify the request:
- UI labels or buttons.
- App store copy.
- Website landing page.
- Social media post or carousel.
- Educational lesson or explainer.
- Legal or policy wording.
- Support message or email.
- Screenshot / design / RTL layout review.

### 2. Check meaning accuracy

Compare source and Arabic draft:
- Same main message preserved.
- No missing warnings, limits, dates, numbers, prices, phone numbers, or calls to action.
- No added claims that were not in the source.
- Technical terms are translated consistently.
- Ambiguous words are flagged instead of guessed.

### 3. Check Arabic naturalness

Review the Arabic for:
- Clear sentence flow.
- Audience-appropriate vocabulary.
- No awkward literal translation.
- No mixed tone within the same paragraph.
- Avoiding unnecessary English when an Arabic term is clearer.
- Preserving brand/product names when they should remain in English.

### 4. Check RTL and design layout

For screenshots or UI/design reviews, verify:
- Arabic text direction is right-to-left.
- Mixed numbers, URLs, emails, and product names remain readable.
- Punctuation appears on the correct side.
- Text is not clipped, overlapped, stretched, or too small.
- Icons match the text meaning and are not mirrored incorrectly.
- Buttons and navigation order make sense for RTL users.
- Line breaks do not split important phrases badly.

### 5. Check bilingual consistency

For Arabic/English pairs:
- Titles match in intent.
- Subtitles and bullets cover the same points.
- Calls to action match.
- Contact details, website links, dates, phone numbers, and prices match exactly.
- Hashtags or keywords are safe and relevant.
- One language is not much longer than the layout can handle.

### 6. Safety and compliance check

Flag and fix:
- Private personal data.
- Secrets, credentials, account recovery codes, or internal URLs.
- Unsupported medical, legal, financial, or security claims.
- Offensive, discriminatory, or culturally insensitive wording.
- Cybersecurity wording that implies unauthorized testing or harmful activity.
- Marketing claims that sound guaranteed or misleading.

## Output format

Default output should be concise:

```text
Status: Ready / Needs edits / Blocked

Main issues:
1. ...
2. ...

Suggested Arabic revision:
...

RTL/layout notes:
...

Final checklist:
- Meaning preserved: yes/no
- Tone suitable: yes/no
- Contact/details match: yes/no
- RTL readable: yes/no
- Safe to publish: yes/no
```

## QA table format

Use this when reviewing multiple strings:

```text
| ID | Source | Arabic draft | Issue | Suggested fix | Severity |
|----|--------|--------------|-------|---------------|----------|
| 1  | ...    | ...          | ...   | ...           | Low/Med/High |
```

Severity guide:
- High: wrong meaning, broken RTL, legal/safety risk, missing required detail.
- Medium: awkward wording, inconsistent term, unclear CTA.
- Low: style polish, punctuation, spacing.

## Reusable localization checklist

Before release, verify:
- All visible strings are translated or intentionally left in English.
- Arabic text is readable at final size.
- Mixed English/Arabic text renders correctly.
- Numbers, dates, phone numbers, emails, URLs, and prices are unchanged.
- Buttons fit without truncation.
- Error messages explain what the user should do next.
- No private data or test placeholders remain.
- Screenshots and captions match the final text.
- The user approves before public publishing or account changes.

## Example prompts

- Review this Arabic app screen for RTL and wording issues.
- Compare this English caption with the Arabic version and tell me if it is ready to publish.
- Improve this Arabic education text for parents while keeping it simple.
- Check this bilingual cybersecurity awareness post for accuracy and safe wording.
- Make a QA table for these Arabic UI strings.

## Boundaries

This skill can draft and review text.
It must not publish, upload, send messages, change live apps, edit production files, or run active cyber testing without explicit approval.

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
