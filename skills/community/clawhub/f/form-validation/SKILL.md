---
name: form-validation
description: Deep form validation workflow—schemas, sync vs async rules, UX patterns, accessibility, and server parity. Use when building complex forms, multi-step wizards, or reducing validation bugs.
---

# Form Validation

Validation combines **correctness** and **UX**: when errors appear, how they are announced, and how client rules match the server.

## When to Offer This Workflow

**Trigger conditions:**

- Long forms, wizards, or multi-step checkouts
- Accessibility audits flagging unclear errors
- Mismatch between client-side “valid” and API rejection

**Initial offer:**

Use **six stages**: (1) model & schema, (2) rule layers, (3) UX timing, (4) accessibility, (5) async & server parity, (6) testing). Confirm framework (React Hook Form, Formik, native, etc.).

---

## Stage 1: Model & Schema

**Goal:** Single schema (Zod, Yup, JSON Schema) as source of truth; share with backend when feasible.

---

## Stage 2: Rule Layers

**Goal:** Separate required/format rules from cross-field rules (e.g., date range); isolate async checks (username available) from fast inline validation.

---

## Stage 3: UX Timing

**Goal:** Choose onBlur vs onSubmit per field; avoid shouting on every keystroke unless real-time feedback is a product requirement.

---

## Stage 4: Accessibility

**Goal:** Associate errors with fields via `aria-describedby`; move focus to first error on submit; use live regions judiciously.

---

## Stage 5: Async & Server Parity

**Goal:** Map API validation errors to fields; handle race conditions on slow networks; idempotent submit with dedupe if needed.

---

## Stage 6: Testing

**Goal:** Unit-test schema; e2e critical paths including server error mapping.

---

## Final Review Checklist

- [ ] Schema aligned or shared with server
- [ ] Validation timing and copy defined
- [ ] Accessible error patterns
- [ ] API errors mapped to UI
- [ ] Tests for schema and flows

## Tips for Effective Guidance

- Server rules always win—document intentional client shortcuts.
- Pair with **ux-writing** for error microcopy.

## Handling Deviations

- Wizards: validate per step and on final submit; persist drafts securely.
