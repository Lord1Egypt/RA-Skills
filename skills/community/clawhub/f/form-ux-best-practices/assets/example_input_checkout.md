# Example Input: Checkout Form Implementation (Current State)

## Goal
- Returning user completes purchase quickly with minimal friction.

## Current structure
- Step 1: Contact info
- Step 2: Shipping address
- Step 3: Payment

## Known issues
- Labels are hidden and placeholders carry full instructions.
- Billing and shipping forms both show by default even when "same as shipping" is checked.
- Card number uses `type="number"`.
- Expiry field uses `type="text"` without format hint.
- CVC field has no helper text.
- ZIP/postal field has no country-aware guidance.
- Submit button says "Continue" on final payment step.

## Validation behavior
- Inline errors only after submit; no per-field feedback on blur.
- Error text appears below fields but summary is missing.
- First invalid field is not focused after submit fail.

## Accessibility/mobile notes
- Several controls have no explicit `<label for>` mapping.
- Tab order skips from email to payment fields on desktop.
- Mobile keyboard for phone and card fields is full text keyboard.
- Touch targets for address autofill suggestions overlap CTA on small screens.

## Trust notes
- No explanation for collecting phone number.
- Security badge appears only in footer, not near payment submit.
