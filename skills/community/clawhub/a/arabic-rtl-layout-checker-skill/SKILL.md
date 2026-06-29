---
name: "Arabic RTL Layout Checker Skill"
version: 0.1.0
slug: "arabic-rtl-layout-checker-skill"
description: "Checks Arabic and bilingual right-to-left layouts for readable ordering, alignment, font support, punctuation, mirroring, and common UI/design mistakes before publishing."
category: "Arabic Localization"
tags:
  - "arabic"
  - "rtl"
  - "localization"
  - "bilingual"
  - "ui-review"
  - "openclaw"
  - "templates"
generated: "2026-06-14"
---

# Arabic RTL Layout Checker Skill

## Purpose
Use this skill to review Arabic, bilingual Arabic/English, and right-to-left (RTL) designs before publishing. It helps catch layout, wording, alignment, font, and mirroring problems in app screens, websites, carousels, PDFs, slides, and social posts.

The goal is practical quality control: make Arabic content readable, natural, correctly ordered, and visually balanced without exposing private data.

## When to use
Use this skill when you need to check:
- Arabic UI screens, landing pages, forms, dashboards, or settings pages.
- Bilingual Arabic/English layouts where each language has its own slide, page, or column.
- Social posts, carousels, posters, infographics, thumbnails, or PDFs.
- Translation/localization drafts before sending them to a client or publishing.
- RTL bugs such as reversed icons, wrong punctuation placement, awkward line breaks, or mixed English numbers inside Arabic text.

## Inputs
Ask the user for only what is needed:
1. The target format: app screen, website, post, PDF, slide, or document.
2. The Arabic text or screenshot to review.
3. The intended audience and dialect if relevant, for example Gulf, formal Arabic, or mixed Arabic/English.
4. Any fixed brand rules: logo placement, colors, phone/email/website, footer, or slogan.
5. Whether the review should be strict, quick, or publish-ready.

Do not request passwords, account access, hidden client data, private documents, OTPs, tokens, or unrelated personal information.

## Review checklist

### 1. Reading direction and structure
- Confirm the main Arabic content flows right to left.
- Check that section order makes sense for Arabic readers.
- Verify Arabic and English versions match in meaning, not just literal word count.
- Make sure numbered steps, bullet lists, and labels are not reversed incorrectly.

### 2. Typography and Arabic shaping
- Confirm Arabic letters are connected correctly and not broken into isolated characters.
- Check that the font supports Arabic properly.
- Avoid fonts that look decorative but reduce readability.
- Ensure line height is comfortable and descenders are not clipped.
- Confirm diacritics, if used, are not colliding with nearby text.

### 3. Alignment and spacing
- Arabic headings and body text should normally align right unless the design has a clear centered layout.
- Keep consistent padding around cards, buttons, and text boxes.
- Avoid crowding Arabic text into narrow boxes because Arabic words can expand differently from English.
- Check that call-to-action buttons and footer text are not clipped.

### 4. Mixed Arabic and English content
- Verify phone numbers, URLs, emails, product names, and acronyms remain readable.
- Check punctuation around mixed text, for example colons, slashes, brackets, and question marks.
- Keep brand names consistent across Arabic and English.
- Avoid accidental direction jumps in lines containing English terms.

### 5. Icons, arrows, and mirroring
- Mirror directional arrows only when the meaning requires direction.
- Do not mirror logos, brand marks, screenshots, QR codes, flags, or recognizable product icons.
- Check that forward/back icons make sense in RTL navigation.
- Confirm mascot or character pointing direction supports the Arabic content, not away from it.

### 6. Translation quality
- Flag literal machine translation that sounds unnatural.
- Prefer short, clear Arabic over long formal sentences for social posts and UI.
- Keep technical terms understandable; add English in parentheses only when useful.
- Verify warnings and security wording do not exaggerate, scare, or promise guarantees.

### 7. Visual consistency
- Compare Arabic and English versions for same topic, same hierarchy, same contact details, and same brand elements.
- Check that logos, phone numbers, email addresses, and website URLs match.
- Compare dimensions/aspect ratios for carousel slides.
- Confirm exported images are sharp and not blurry from resizing.

## Output format
Return a concise review in this structure:

```text
RTL Review: [Ready / Needs Fix / Blocked]

Main findings:
1. [Issue or OK item]
2. [Issue or OK item]
3. [Issue or OK item]

Fixes:
- Must fix before publish: [...]
- Nice to improve: [...]

Final recommendation:
[Publish / revise first / send me the corrected version]
```

## Severity levels
- BLOCKER: wrong meaning, unreadable Arabic, broken shaping, missing required contact detail, cropped key text, or Arabic/English mismatch that could mislead users.
- FIX: awkward wording, inconsistent alignment, weak spacing, or icon direction problem.
- POLISH: small style improvements that do not block publishing.
- OK: checked and acceptable.

## Example prompts
- Review this Arabic Instagram slide for RTL readability and publishing blockers.
- Compare the English and Arabic versions of this carousel and tell me if they are consistent.
- Check this app settings screen for Arabic alignment, mixed English terms, and mirrored icons.
- Make this Arabic CTA shorter and more natural for Gulf audience.
- Give me a publish-ready checklist for a bilingual Arabic/English PDF.

## Safe boundaries
- This skill reviews content and layout only.
- It does not publish, upload, send, or change account settings.
- It does not handle secrets, private credentials, or unauthorized documents.
- For cybersecurity content, keep wording defensive, legal, and authorization-based.

## Support / Donate
If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
