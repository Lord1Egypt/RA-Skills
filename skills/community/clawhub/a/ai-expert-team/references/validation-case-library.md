# Validation Case Library

Use this reference when validating or extending the `ai-expert-team` skill itself. The goal is to turn each validation run into reusable proof, not a one-off success story.

## Case Log Shape

Each validation case should preserve:

- Input problem.
- Case status and date.
- Case verdict: PASS, FAIL, or PARTIAL for whether the workflow satisfied the case criteria.
- Evidence verdict: PASS, FAIL, or PARTIAL for how strong the supporting proof is.
- Scope and out-of-scope boundaries.
- Selected CEO profile and why it fits.
- CEO honest boundaries and blind spots.
- Rejected CEO profiles and why they were rejected.
- Selected specialists with source paths.
- Rejected specialists and why they were rejected.
- Task routing plan.
- Evidence checked, including commands and observed output when available.
- Expert reports using the standard output contract.
- CEO challenge questions and answers.
- Final synthesis with verified findings, consensus, disagreements, open risks, and next actions.
- Checklist proving all required fields were recorded.

## Verdict Discipline

Do not collapse all validation into one happy label.

- **Case verdict** answers: did this workflow satisfy the stated validation case requirements?
- **Evidence verdict** answers: how strong is the proof behind the conclusion?

Example: a product strategy case can PASS the workflow requirement while still having PARTIAL evidence when external market evidence is intentionally out of scope.

## Recommended Validation Sequence

1. **Complex technical case**
   - Proves artifact availability, internal protocol consistency, reference/template existence, and command-backed verification.
   - Should cite files, commands, and a verification verdict.

2. **Product / strategy case**
   - Proves CEO lens selection, blind spot handling, contrarian/risk review, and concrete next action.
   - Keep market proof explicitly PARTIAL unless supported by user research, analytics, install data, or external evidence.

3. **Wrong-routing failure case**
   - Proves honest boundaries, availability gates, or verification can correct an initially tempting but wrong CEO or specialist choice.
   - If routing fails, record the exact routing rule to fix.

## Product Strategy Lesson

When deciding the next growth path for an agent skill, prefer this sequence unless new evidence overrides it:

1. Build a validation-case library first.
2. Use validation findings to guide Hermes-native polish.
3. Keep ClawHub distribution claims bounded to the evidence collected in the current cycle.

Reason: examples create trust and reveal workflow defects; polish before examples can optimize the wrong path; distribution claims beyond proof create attention without confidence.

## Common Pitfalls

- Treating ClawHub search visibility as broader distribution proof.
- Calling a strategy fully validated without external user evidence or analytics.
- Letting a validation page become long-form prose without runnable inputs, rosters, verdicts, and next actions.
- Forgetting to record rejected CEOs or specialists, which hides routing quality.
- Omitting CEO challenge questions even though the skill requires CEO challenge before synthesis.
