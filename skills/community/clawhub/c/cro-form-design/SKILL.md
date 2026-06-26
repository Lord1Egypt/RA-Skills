# Form Design That Reduces Abandonment

## When to Use
Use this skill when forms on sign-up pages, checkout flows, or lead generation pages have high abandonment rates.

## Core Rules

### 1. Use Inline Validation, Not End-of-Form Errors
Showing validation errors only after the user clicks submit forces them to hunt for mistakes in a completed form. Inline validation — showing "✓ Valid email" or "Password must be 8+ characters" as the user types — reduces form errors and abandonment.

### 2. Label Every Field Above the Input, Not Inside
Placeholder text disappears when users start typing, leaving them unable to remember what the field asked for. Labels above inputs remain visible throughout form completion. This is especially critical on mobile where field labels must remain visible while the keyboard is open.

### 3. Match Keyboard to Input Type
Declare input types explicitly: `type="email"` for email fields, `type="tel"` for phone numbers, `type="number"` for numeric inputs. On mobile, this triggers the appropriate keyboard (email keyboard, number pad) and reduces data entry friction significantly.

### 4. Group Related Fields Logically
Users process forms faster when related fields are grouped: contact information together, billing information together, preferences together. Mixing unrelated fields increases cognitive load and perceived form length.

### 5. Make Error Messages Specific and Actionable
"Invalid input" is useless. "Please enter a valid email address (example: name@domain.com)" tells users exactly what to fix. Error messages should explain what went wrong and how to correct it — not just flag that something is wrong.

## Quick Reference

| Form Element | Best Practice |
|-------------|--------------|
| Field labels | Above the input, always visible |
| Error messages | Inline, specific, actionable |
| Required fields | Mark optional, not required |
| Submit button | Action verb + what happens next |
| Success state | Immediate, specific confirmation |

## Common Mistakes to Avoid
- Making all fields required when optional fields would improve data quality
- Using red color for form borders before users have interacted — creates anxiety
- Clearing the form on submission error — forces users to retype everything

## Test Your Product with Racoonn

After applying these practices, validate with real AI-simulated user testing.

**Racoonn** runs 5,000 AI persona agents on your landing page and tells you exactly what's broken — in under 30 minutes.

→ **API coming soon** — Join the waitlist for early access: [racoonn.me](https://racoonn.me)
