---
name: 前端主题工程师-国际化与用户提示
description: Frontend theme engineer skill for i18n-compliant user text, translation files, and framework-safe user notification patterns.
version: 1.0.0
---

# Role

This skill owns user-facing copy, translation wiring, and friendly notification patterns in the Weline view layer. It ensures templates, tag attributes, and client-side feedback remain translatable and framework-compliant.

# When To Use

- Use for labels, placeholders, buttons, messages, modal copy, toasts, and translation files.
- Use for keywords such as i18n, translation, `__()`, `<lang>`, `@lang`, toast, confirm, prompt, and user feedback.
- Use when a frontend or backend UI change introduces or modifies visible text.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/i18n-internationalization/SKILL.md`
- `dev/ai/skills/friendly-notifications/SKILL.md`
- `dev/ai/skills/theme-development/SKILL.md`
- `dev/ai/skills/frontend-components/SKILL.md`

# Responsibilities

- Move user-facing text into the correct i18n mechanism.
- Use attribute-safe translation expressions in custom tags and templates.
- Replace blocking browser dialogs with framework notification or confirmation components.
- Keep visible error messages actionable and understandable.

# Workflow

1. Identify every new or changed user-facing string in the target UI path.
2. Choose the right translation form for PHP, plain template markup, or custom-tag attributes.
3. Update the owning `i18n` files when new text keys are introduced.
4. Replace browser-native dialogs with framework-safe toasts or confirmation components.
5. Review message wording for clarity, actionability, and consistency.
6. Validate the UI path where the text or notification appears.
7. Report any missing translation coverage or UX copy risks.

# Weline Rules

- Do not hardcode user-facing text.
- Use i18n for user-facing text.
- Use `@lang` forms in custom-tag attributes instead of embedded PHP.
- Do not use JavaScript `alert`, `confirm`, or `prompt`.
- Keep placeholders in `%{1}` or `%{name}` style where interpolation is required.

# Inputs Required

- The UI path and template or component where text appears.
- The language files or translation domain in use.
- The desired feedback behavior for success, warning, confirmation, or failure.
- Validation route or screen.

# Expected Output

- Updated templates, translations, or notification calls with framework-safe patterns.
- Visible-text coverage that is ready for translation.
- Validation evidence from the UI surface that shows the message or prompt behavior.

# Validation

- Confirm new or changed visible text is translated through the correct mechanism.
- Confirm custom-tag attributes do not contain embedded PHP translation calls.
- Confirm user prompts use framework toasts or confirmation UI instead of browser-native dialogs.
- Confirm interpolation placeholders follow repository conventions.

# Constraints

- Do not leave literal user-facing strings in templates or scripts.
- Do not embed PHP into custom-tag attributes for translation.
- Do not use blocking browser dialogs.
- Do not treat translation files as optional when visible text changed.

