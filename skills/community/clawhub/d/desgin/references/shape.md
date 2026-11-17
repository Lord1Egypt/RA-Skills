# Shape — Plan Before Building

`shape` is the planning command. Use it before writing any UI code.

## Inputs

- Brief or user intent.
- Existing design files, if any.
- Target framework (Angular, React, Blazor, or unknown).
- Primary viewport (default: mobile).

## Outputs

A short design plan with:

1. **Subject and audience:** what the product is and who uses it.
2. **Mode:** Persuade, Operate, Read, or Experience.
3. **Visual direction:** 4–6 color tokens, typefaces, and a one-sentence layout concept.
4. **Mobile-first wireframe:** ASCII or text description of the 375px layout.
5. **Breakpoints:** where the layout shifts and why.
6. **Component list:** the main components needed, with variants.
7. **Risk callouts:** accessibility, performance, or framework-specific concerns.

## Steps

1. Ask the clarifying questions: subject, audience, framework, primary action.
2. Propose 2–3 visual directions with tradeoffs.
3. Get user approval before writing code.
4. Write the plan to `docs/design/{feature}-design.md` or similar project location.

## Constraints

- No code until the plan is approved.
- No placeholder text like "TBD" or "we will decide later."
- Every decision must be traceable to the brief or a design principle.
