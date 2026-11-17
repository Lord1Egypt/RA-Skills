# Alignment, Rebaseline, Audit, And Finish Line 2.1

Use one authority mode per pass. Direction checks do not silently rewrite targets, and audits do not sign acceptance.

## Lightweight Stage Alignment

At every stage record:

1. the user or operator change;
2. the target and criterion served;
3. scope, assumption, or architecture movement;
4. evidence against premature completion;
5. whether the next action is still the highest-value authorized action.

Keep this to a concise Loop delta.

## Formal Alignment

Run after stages 3, 6, and 10, and immediately when:

- the authority fingerprint changes;
- estimated scope grows by more than 20 percent;
- a primary user flow fails behind green automatic checks;
- the target link cannot be stated in one sentence;
- the same failure signature produces no new evidence twice;
- the same material risk is carried twice;
- three consecutive final decisions are `Accepted With Risk`;
- a new idea affects target, Non-Goals, protected architecture/data, release, or production behavior.

Verdicts:

- `Aligned - Continue`
- `Aligned - Ready for Independent Acceptance`
- `At Risk`
- `Locally Compliant, Globally Misaligned`
- `Owner Review Required`
- `Blocked`

Formal alignment may resize, split, pause, or request an Owner decision. It does not authorize a target change by itself.

## Idea Intake

Classify new ideas as `Observation`, `Clarification`, `Improvement Candidate`, `Scope Change`, `Core Target Change`, or `Conflict`. Only a clarification that leaves acceptance and Non-Goals unchanged may enter active work immediately.

## Target Rebaseline

Compare the previous target, new request, user value, work preserved or invalidated, acceptance changes, cost, risk, and Owner decisions. Return one of:

- `No Target Change`
- `Clarification Only`
- `Scope Change Approved`
- `Core Target Change Approved`
- `Owner Decision Required`
- `Reject / Defer`

Do not implement or dispatch during the rebaseline pass. After approval, update authority, regenerate the fingerprint, then run a separate Planning/Dispatch pass.

## Whole-Project Audit

Audit is read-only by default and may use a broader explicit context budget. Separate verified facts, missing evidence, risk debt, contradictory claims, local success without global value, and Owner decisions. Contract consistency, artifact presence, and runtime usability must be scored separately.

## Finish Line

Define the original outcome, current user-visible capability, Must Finish, Not Required Now, work to stop expanding, next independently valuable delivery, and final evidence. A Milestone closes only when a coherent capability receives the required acceptance.
