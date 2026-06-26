# Form UX Canon (Paraphrased Rules)

## Luke Wroblewski (Web Form Design)
- Keep forms as short as the decision allows.
- Prefer single-column flows to reduce scanning errors.
- Align labels consistently and keep them persistent while typing.
- Move from easy fields to harder fields to maintain momentum.
- Reduce unnecessary interruptions between user intent and submit.

## Caroline Jarrett & Gerry Gaffney (Forms that Work)
- Treat forms as conversations with a clear user purpose.
- Ask only questions you can act on.
- Phrase labels the way users think about their own data.
- Put instructions where they are needed, not in long preambles.
- Validate based on realistic user behavior, not idealized input paths.

## Adam Silver (Form Design Patterns)
- Use familiar patterns for names, addresses, payments, and auth.
- Ask one thing per field and avoid overloaded labels.
- Make errors easy to correct with specific examples.
- Prefer explicit optional markers over ambiguous required hints.
- Design for edge cases early (long names, international addresses, odd but valid input).

## Nielsen Norman Group (Form Guidelines + Error Messaging)
- Match field order to user expectations and task sequence.
- Prevent errors when possible, then recover clearly when they occur.
- Keep error placement near affected fields and summarize globally for long forms.
- Avoid hidden rules; surface constraints before submission.
- Preserve user-entered values after failed submission.

## Baymard Institute (E-commerce Forms)
- Use generous defaults and autofill-compatible attributes for checkout speed.
- Avoid unnecessary address and payment friction.
- Distinguish billing vs shipping only when needed.
- Use clear field labels for card details and avoid ambiguous abbreviations.
- Reduce account-creation pressure during checkout unless essential.

## GOV.UK Design System (Validation + Error Summary)
- Show an error summary at top when submit fails with multiple issues.
- Link each summary item to the relevant field.
- Keep error message text consistent between field-level and summary-level copy.
- Place error text next to the field label so users do not miss context.
- Move focus to the summary after failed submission.

## WCAG Concepts (Error Identification + Suggestion)
- Identify errors in text and indicate which field has the issue (WCAG 3.3.1).
- Provide correction guidance when user input can be fixed (WCAG 3.3.3).
- Keep label/instruction relationships explicit and machine-readable (WCAG 1.3.1).
- Ensure full keyboard operation (WCAG 2.1.1).
- Keep focus order logical and predictable (WCAG 2.4.3).
- Expose field states and messaging to assistive tech via proper semantics (WCAG 4.1.2).

## Tradeoff Rule: Live Validation
- Use immediate validation only when it reduces rework and avoids noise.
- Delay validation for required/format checks until blur or submit when early errors would distract.
- For high-risk fields (password, username uniqueness), combine lightweight live cues with definitive submit-time checks.
