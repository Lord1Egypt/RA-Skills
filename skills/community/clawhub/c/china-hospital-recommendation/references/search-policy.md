# Search Policy

## Search Scope

Use search only for dynamic information that may change:

- hospital international service pages
- administrative intake workflow for foreign patients
- pre-travel record-review workflow
- doctor-led remote consultation workflow for first contact
- department pages
- specialist or department-lead public profiles
- JCI certification status and last public verification signal
- visa guidance
- transportation planning
- accommodation planning

## Do Not Search

- Fudan rankings themselves
- static product definition
- the report template

Those must come from bundled skill references.

## Source Priority

Prefer sources in this order:

1. official hospital websites
2. official university or affiliated medical center pages
3. official government or embassy pages
4. reputable public institution pages

Use lower-confidence sources only when the report explicitly marks them as provisional.

## Failure Handling

- If a dynamic fact cannot be confirmed, omit it or move it to `current_checks`.
- If JCI status cannot be confirmed, say `Not currently verified` rather than implying a negative quality judgment.
- If a specialist profile is weakly evidenced, write a specialist direction instead of a person name.
- Treat administrative intake, record-review workflow, and doctor-led remote consultation as separate evidence questions.
- Do not imply that doctor-led remote consultation is available unless a public source clearly supports that exact claim.
- If only part of the access path is evidenced, write `Needs manual confirmation` for the unverified steps instead of smoothing the language.
- Add a note in `evidence_notes` when a delivery still needs manual verification.
