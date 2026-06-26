# Top Issues (P0/P1/P2)

| Priority | Issue | Impact | Rationale | Fix |
| --- | --- | --- | --- | --- |
| P0/P1/P2 | [Issue summary] | [User/business impact] | [Why this matters now] | [Concrete remediation] |

# Field-by-field rewrite

| Field | Label | Helper text | Placeholder policy | Validation copy |
| --- | --- | --- | --- | --- |
| [field_id_or_name] | [final label] | [supporting guidance] | [none/example-only/format hint] | [error message(s)] |

# Validation & error messaging spec

## Timing strategy
- Required checks: [on submit / on blur / both]
- Format checks: [on blur / threshold-based live / on submit]
- Server checks: [when and how to surface]

## Inline error behavior
- Trigger: [event]
- Placement: [near label / helper region]
- Content format: [specific recovery guidance]
- Field state hooks: [`aria-invalid`, `aria-describedby` references]

## Submit-time failure behavior
- Block submit when: [conditions]
- Preserve user input: [yes/no and exceptions]
- Focus behavior: [first invalid field or summary first]

## Error summary pattern (when relevant)
- Use summary when: [long forms, multiple simultaneous errors, off-screen errors]
- Summary title: [for example: "There is a problem"]
- Each summary item must: [match inline copy and link to field]

# Accessibility checklist (WCAG-mapped)

- [ ] WCAG 3.3.1 Error Identification: each invalid field has explicit text error.
- [ ] WCAG 3.3.3 Error Suggestion: each error includes how to recover.
- [ ] WCAG 1.3.1 Info and Relationships: labels/instructions/errors are programmatically associated.
- [ ] WCAG 2.1.1 Keyboard: full completion and correction is keyboard-only.
- [ ] WCAG 2.4.3 Focus Order: focus follows logical reading and interaction sequence.
- [ ] WCAG 4.1.2 Name, Role, Value: control state and error state are exposed to assistive tech.

# Ship-ready checklist

- [ ] Every interactive field has a visible label.
- [ ] Every label is programmatically associated with its control.
- [ ] Required vs optional status is explicit and consistent.
- [ ] Placeholder text is not the only source of field meaning.
- [ ] `name` attributes exist for submitted controls.
- [ ] Input types and `inputmode` match expected data entry.
- [ ] `autocomplete` is set for common personal/contact/payment fields.
- [ ] Helper text is short, specific, and adjacent to relevant fields.
- [ ] Inline errors use specific recovery language.
- [ ] Error summary appears on failed submit when multiple errors can occur.
- [ ] Error summary links move focus to related fields.
- [ ] Invalid fields expose `aria-invalid="true"` after failure.
- [ ] Error/helper references are wired with `aria-describedby`.
- [ ] Keyboard tab order matches visual order.
- [ ] Form state persists user input after failed submit.
- [ ] Sensitive fields include just-in-time trust/privacy cues.
- [ ] Consent language distinguishes required vs optional consent.
- [ ] Final submit CTA is specific to user intent (not generic "Submit").

# Optional: Ready-to-ship snippet

```html
<!-- Optional semantic HTML or React pseudo-code snippet goes here -->
```
