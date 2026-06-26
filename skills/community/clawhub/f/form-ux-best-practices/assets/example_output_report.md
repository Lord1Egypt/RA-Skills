# Top Issues (P0/P1/P2)

| Priority | Issue | Impact | Rationale | Fix |
| --- | --- | --- | --- | --- |
| P0 | Missing programmatic label associations on key checkout fields | Screen-reader users cannot reliably identify fields; completion can fail entirely | Violates core accessibility semantics and creates legal/compliance exposure | Add visible labels and bind each via `for`/`id`; wire helper/error text with `aria-describedby` |
| P1 | Generic and delayed validation copy without error summary | Users cannot quickly recover from failures; abandonments increase on long forms | Recovery cost rises when users must hunt for multiple errors | Add specific inline error copy plus submit-time error summary linking to each invalid field |
| P1 | Incorrect input types and missing autocomplete on contact/payment fields | Mobile entry slows down and typo rate increases | Keyboard mismatch and missing autofill cues add friction | Use semantic `type`/`inputmode` and set `autocomplete` tokens (`email`, `tel`, `cc-number`, etc.) |
| P2 | Optional/required rules are unclear for phone and marketing consent | Users hesitate and may provide low-quality data | Ambiguity adds cognitive load and trust friction | Mark optional explicitly, explain why phone is requested, and separate required vs marketing consent |

# Field-by-field rewrite

| Field | Label | Helper text | Placeholder policy | Validation copy |
| --- | --- | --- | --- | --- |
| email | Work email | We'll send receipts and account updates here. | Placeholder optional example only: `name@company.com` | "Enter a valid work email, for example name@company.com." |
| phone | Phone number (optional) | Used only for delivery questions related to this order. | No placeholder; rely on label + helper text | "Enter a valid phone number including country/area code." |
| cc_number | Card number | Cards accepted: Visa, Mastercard, AmEx. | Optional format hint: `1234 1234 1234 1234` | "Enter a valid card number." |
| cc_exp | Expiration date | Format: MM/YY. | Placeholder may show `MM/YY`. | "Enter expiration date in MM/YY format." |
| cc_csc | Security code | 3 or 4 digits on your card. | No placeholder required. | "Enter the 3- or 4-digit security code." |
| postal_code | Postal code | Must match delivery country. | Optional example based on selected country. | "Enter a valid postal code for the selected country." |

# Validation & error messaging spec

## Timing strategy
- Required checks: on submit, with per-field reminders after submit attempt.
- Format checks: on blur for email, phone, card fields; avoid first-keystroke errors.
- Server checks: run after local pass; map server failures to field-specific messages when possible.

## Inline error behavior
- Trigger: on blur after interaction, and on submit for untouched invalid fields.
- Placement: directly below label/helper region.
- Content format: "What went wrong + how to fix it" in one sentence.
- Field state hooks: set `aria-invalid="true"`; add error ID to `aria-describedby`.

## Submit-time failure behavior
- Block submit when: required fields missing or format checks fail.
- Preserve user input: yes, except masked/security-sensitive values if policy requires re-entry.
- Focus behavior: move focus to error summary first, then follow linked item to first invalid field.

## Error summary pattern (when relevant)
- Use summary when: 2+ errors can appear or when form length causes off-screen errors.
- Summary title: "There is a problem with your submission".
- Each summary item must: match inline message text and link to the invalid field.

# Accessibility checklist (WCAG-mapped)

- [x] WCAG 3.3.1 Error Identification: each invalid field has explicit text error.
- [x] WCAG 3.3.3 Error Suggestion: each error includes how to recover.
- [x] WCAG 1.3.1 Info and Relationships: labels/instructions/errors are programmatically associated.
- [x] WCAG 2.1.1 Keyboard: full completion and correction is keyboard-only.
- [x] WCAG 2.4.3 Focus Order: focus follows logical reading and interaction sequence.
- [x] WCAG 4.1.2 Name, Role, Value: control state and error state are exposed to assistive tech.

# Ship-ready checklist

- [x] Every interactive field has a visible label.
- [x] Every label is programmatically associated with its control.
- [x] Required vs optional status is explicit and consistent.
- [x] Placeholder text is not the only source of field meaning.
- [x] `name` attributes exist for submitted controls.
- [x] Input types and `inputmode` match expected data entry.
- [x] `autocomplete` is set for common personal/contact/payment fields.
- [x] Helper text is short, specific, and adjacent to relevant fields.
- [x] Inline errors use specific recovery language.
- [x] Error summary appears on failed submit when multiple errors can occur.
- [x] Error summary links move focus to related fields.
- [x] Invalid fields expose `aria-invalid="true"` after failure.
- [x] Error/helper references are wired with `aria-describedby`.
- [x] Keyboard tab order matches visual order.
- [x] Form state persists user input after failed submit.
- [x] Sensitive fields include just-in-time trust/privacy cues.
- [x] Consent language distinguishes required vs optional consent.
- [x] Final submit CTA is specific to user intent ("Place order").

# Optional: Ready-to-ship snippet

```html
<form novalidate aria-describedby="checkout-error-summary">
  <div id="checkout-error-summary" role="alert" tabindex="-1" hidden>
    <h2>There is a problem with your submission</h2>
    <ul>
      <li><a href="#email">Enter a valid work email, for example name@company.com.</a></li>
      <li><a href="#cc_number">Enter a valid card number.</a></li>
    </ul>
  </div>

  <label for="email">Work email</label>
  <input id="email" name="email" type="email" autocomplete="email" aria-describedby="email-help email-error" />
  <p id="email-help">We'll send receipts and account updates here.</p>
  <p id="email-error" hidden>Enter a valid work email, for example name@company.com.</p>

  <label for="cc_number">Card number</label>
  <input id="cc_number" name="cc_number" type="text" inputmode="numeric" autocomplete="cc-number" aria-describedby="cc-number-help cc-number-error" />
  <p id="cc-number-help">Cards accepted: Visa, Mastercard, AmEx.</p>
  <p id="cc-number-error" hidden>Enter a valid card number.</p>

  <button type="submit">Place order</button>
</form>
```
