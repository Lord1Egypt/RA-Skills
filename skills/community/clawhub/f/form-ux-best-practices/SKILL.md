---
name: form-ux-best-practices
description: Opinionated form UX and accessibility workflow for signup, checkout, settings, and lead-gen forms. Use when reviewing a form spec or existing implementation to produce prioritized UX/accessibility/copy fixes, field-by-field rewrites, validation and error messaging specs, and optional ready-to-ship HTML/React pseudo-code. Do not use for purely visual redesigns, non-form screens, or analytics-only audits.
---

# Form UX Best Practices

## Operating Mode
- Run in text-only mode by default.
- Avoid image-led critiques, dashboards, or visual redesign directions unless explicitly requested.
- Prioritize decisions that improve completion quality, error recovery, accessibility, and trust.

## Inputs Required
Collect these inputs before reviewing:
- Form context: signup, checkout, settings, lead-gen, or other.
- Primary business goal and user goal.
- Current form source: spec, HTML, React, screenshots transcribed to text, or mixed.
- Field list with required/optional status.
- Current validation behavior (inline, blur, submit, server-side).
- Target devices (desktop, mobile, both).

## Intake Questions
Ask only if essential inputs are missing. If essentials are present, proceed without questions.
- What is the exact decision this form should support (create account, complete purchase, update settings, capture lead)?
- Which fields are mandatory to complete that decision?
- What happens after submit (success path, retry path, abandonment path)?
- Are there legal or policy constraints (age checks, billing details, consent, regional rules)?

## Deterministic Review Workflow
1. Define task-critical outcome: state one sentence for user success and one sentence for business success.
2. Map friction points: identify every extra field, ambiguous label, avoidable decision, and interruption.
3. Audit field architecture: check sequence, grouping, required/optional clarity, and progressive disclosure.
4. Audit validation behavior: check timing, specificity, recovery path, and consistency between inline and submit states.
5. Audit accessibility semantics: labels, instructions, focus order, keyboard use, and error associations.
6. Audit mobile ergonomics: input type, inputmode, keyboard hints, spacing, touch target comfort, and scroll/focus behavior.
7. Audit trust signals: explain why sensitive fields are requested and place privacy assurances at decision moments.
8. Produce outputs using `assets/report_template.md` exactly.

## Reference Loading
- Load `references/canon.md` only when you need principle-level rationale or a tie-breaker between competing form patterns.
- Prefer the deterministic workflow above for execution; use canon references to justify recommendations, not to replace direct analysis.

## Accessibility Checks
- Ensure every control has a programmatic name from a visible label, not placeholder-only text.
- Ensure `label` and control association via `for`/`id` or explicit wrapper label pattern.
- Ensure helper text and errors are referenced by `aria-describedby` where applicable.
- Ensure invalid fields set `aria-invalid="true"` after validation fails.
- Ensure error summary (if used) links to each invalid field and receives focus after failed submit.
- Ensure tab/focus order matches visual/logical order.
- Ensure keyboard-only completion is possible without pointer interaction.

## Mobile Checks
- Use the correct keyboard hints (`type`, `inputmode`, `autocomplete`, `autocapitalize`).
- Keep label visibility persistent while typing.
- Avoid multi-column field arrangements that compress touch targets on narrow screens.
- Keep helper/error text close to field and visible without horizontal scrolling.
- Avoid forced context-switch loops (field blur -> jump -> keyboard close/open thrash).

## Validation Strategy
- Validate required presence on submit, not on first keystroke.
- Validate format either on blur or when enough characters exist to infer intent.
- Reserve real-time validation for high-value, low-noise cases (for example: password strength meter, username availability).
- Show one clear recovery action per error.
- Keep inline error copy consistent with submit-time error summary copy.
- Use error summary for multi-error forms or long forms where first error may be off-screen.

## Field Design Rules
- Prefer explicit labels above fields; do not rely on placeholders as labels.
- Mark optional fields explicitly; keep required as default unless product policy requires explicit required badges.
- Request only minimum data needed for the current decision.
- Group related fields and follow user mental model order (for checkout: contact -> delivery -> payment).
- State constraints before input when predictable (format, length, character rules).

## Microcopy Rules
- Use direct, specific phrasing that names the issue and next action.
- Avoid blame language and vague statements like "Invalid input".
- Mention accepted format when format errors are common.
- Keep tone neutral and recovery-oriented.
- Keep labels and error terms consistent (same field name in label, helper, and error).

## Privacy and Trust Cues
- Explain why sensitive information is needed at the moment it is requested.
- Place trust cues near commitment actions (submit/place order), not buried in footer text.
- Clarify consent scope and frequency for communications fields.
- Separate mandatory operational consent from optional marketing consent.

## Conversion and Friction Rules
- Remove non-essential fields from initial flow.
- Use progressive disclosure for secondary details.
- Prefer smart defaults when safe and reversible.
- Preserve entered values after failed submit.
- Minimize redundant confirmation fields unless risk justifies it.

## Prioritization Rubric (P0/P1/P2)
- P0: Blocks completion, creates legal/compliance risk, or makes the form unusable for assistive tech.
- P1: Causes significant confusion, avoidable errors, or measurable abandonment risk.
- P2: Improves clarity, speed, and polish but does not block completion.

## Output Format
Always fill `assets/report_template.md` sections in this exact order:
1. Top Issues (P0/P1/P2)
2. Field-by-field rewrite
3. Validation & error messaging spec
4. Accessibility checklist
5. Ship-ready checklist
6. Optional: Ready-to-ship snippet

## Optional Ship Snippet Mode
When asked to produce implementation-ready guidance:
- Output either semantic HTML or React pseudo-code.
- Include labels, helper text hooks, error bindings, and `autocomplete` attributes.
- Include submit-time summary pattern when there are 2+ possible simultaneous errors.
- Keep snippet focused on form behavior and semantics, not visual styling.

## Optional Static Audit Script
Use `scripts/form_audit.py` for quick static checks on HTML forms.

```bash
python3 scripts/form_audit.py /path/to/form.html
```

Script checks:
- Missing label mapping
- Duplicate IDs
- Missing `name` attributes
- Placeholder used as label
- Missing autocomplete for common fields
- Likely input type mismatches
