# Example Input: Signup Form Spec (Current State)

## Goal
- User creates an account to start a free trial.

## Current fields
1. Name (placeholder only: "Full name")
2. Email (label says "Contact")
3. Password (no requirements shown)
4. Confirm password
5. Company (required)
6. Phone (optional but not marked optional)
7. "How did you hear about us?" dropdown (required)
8. Marketing opt-in checkbox (pre-checked)

## Current behavior
- Validation runs on every keystroke for all fields.
- Errors are generic ("Invalid field").
- On submit fail, page reloads and clears password fields.
- No top-level error summary.

## Implementation notes
- Email field uses `type="text"`.
- Phone field uses `type="text"` with no `inputmode`.
- No `autocomplete` attributes.
- Several inputs have no `name` attributes.
- One input ID (`field-input`) is reused across three fields.

## Trust/privacy
- No explanation for why phone is requested.
- No link to privacy terms near opt-in.

## Devices
- Desktop and mobile web.
