---
name: "Arabic Family App RTL Skill"
version: 0.1.0
slug: "arabic-family-app-rtl-skill"
description: "Review Arabic-first family and mobile apps for RTL layout, bilingual copy, onboarding, approval flows, and safe local-first defaults."
category: "Arabic Apps & Localization"
tags:
  - "arabic"
  - "rtl"
  - "bilingual"
  - "mobile-apps"
  - "localization"
  - "family-apps"
  - "openclaw"
generated: "2026-06-16"
---

# Arabic Family App RTL Skill

## Purpose

Use this skill to review, plan, or QA Arabic-first family and community apps. It focuses on right-to-left layout, Arabic/English bilingual copy, onboarding, invite or approval flows, privacy, and local-first/demo-safe behavior.

It is especially useful for React Native, Expo, Flutter, web apps, and no-code prototypes that need Arabic as the default user experience.

## When to use

Use this skill when the user asks to:

- Review an Arabic-first app screen or feature.
- Convert an English UI flow into Arabic/RTL.
- Check Arabic copy, labels, empty states, buttons, and validation messages.
- Plan onboarding, registration, invite-only access, or admin approval flows.
- Verify family/community app privacy rules before adding backend sync.
- Prepare a concise handoff for a coding agent without exposing secrets.

## Inputs

Ask for or use the safest available inputs:

- App goal and audience.
- Screen name or feature name.
- Default language and secondary language.
- Screenshot, route/component path, or pasted UI text.
- Known constraints: private family app, kids excluded/included, admin approval, local/demo mode, Supabase/Firebase/backend status.

Never request passwords, OTPs, private keys, live family data, or production database credentials.

## Review checklist

### 1. RTL layout

- Arabic screens use RTL direction consistently.
- Icons that imply direction are mirrored only when appropriate.
- Back arrows, progress indicators, tabs, cards, and form fields feel natural in RTL.
- Mixed Arabic/English text does not break number, email, URL, or phone formatting.
- Long Arabic names wrap cleanly and do not overlap icons or buttons.

### 2. Arabic copy quality

- Main labels are short and natural, not literal machine translations.
- Buttons use action verbs and clear outcomes.
- Error messages explain what to fix without blaming the user.
- Empty states tell the user what happens next.
- Sensitive family/community wording is respectful and private.

### 3. Bilingual consistency

- English and Arabic screens describe the same feature and status.
- Required fields match in both languages.
- Dates, phone numbers, emails, and family names remain readable.
- The app never mixes hardcoded English inside Arabic user-facing screens unless intended.

### 4. Onboarding and registration

- The first-run flow explains what the app is, who can join, and who approves access.
- If invite-only, the invite-code step appears before collecting unnecessary personal data.
- Pending, rejected, and approved states are clear.
- Logout or contact-admin options are available when the user is blocked.

### 5. Admin approval and privacy

- Admin-only actions are hidden from normal members.
- Approval/rejection flows are reversible where possible.
- Private family data is not shown to unapproved users.
- Kids/guardian flows are either fully implemented or clearly deferred; no half-enabled unsafe path.
- The UI distinguishes demo data from real private data when useful.

### 6. Local-first and backend safety

- The app can run safely without backend environment variables if that is a product goal.
- Missing Supabase/Firebase keys should not crash the app.
- Backend migrations, RLS policies, or production writes are not run without explicit approval.
- Demo profiles, mock data, and local storage are clearly separated from live data.

## Output format

Return a concise review:

```text
Status: Ready / Needs fix / Blocked
Screen or feature: ...

What works:
- ...

Needs fix:
- ...

Arabic/RTL notes:
- ...

Privacy/backend notes:
- ...

Best next step:
- ...
```

## Coding-agent handoff template

```text
Task: Improve Arabic/RTL behavior for [screen/feature].
Scope: Only change [files/components].
Keep: Arabic default, RTL support, local/demo fallback, no secrets, no production DB changes.
Check:
1. Arabic labels and empty states.
2. RTL spacing/alignment.
3. English/Arabic key parity.
4. TypeScript/build check.
Stop before: backend migration, account changes, publishing, or destructive edits.
```

## Safety rules

- Do not expose private family information in examples.
- Do not print `.env` files or secrets.
- Do not run production migrations, publish app builds, or upload data without approval.
- Do not activate kids/chat/payment features unless the user explicitly approved them.
- Prefer small, reviewable changes with a real verification command.

## Example prompts

- Review this Arabic family app screen for RTL and privacy issues.
- Create a bilingual onboarding checklist for an invite-only family app.
- Prepare a Cursor handoff to fix Arabic labels and RTL spacing in this Expo screen.
- Compare Arabic and English translation keys for missing user-facing strings.

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
