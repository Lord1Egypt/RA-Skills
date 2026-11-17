# Goal Discovery 2.1

Use when the user knows a concept, pain, direction, or desired result but not the implementation path.

## Low-Burden Interview

Ask at most three questions per round and only when answers materially change the desired outcome, beneficiary, minimum useful workflow, observable success, safety/privacy/data/cost boundary, or an expensive irreversible choice. Do not ask a non-technical user to select frameworks or architecture unless the choice changes user-visible tradeoffs.

When the user does not know, provide two or three plain-language options, state the practical difference, recommend one reversible default, and label it as an AI assumption. Do not repeat facts already available in the conversation or repository.

## Intent Model

Separate desired outcome, beneficiary and situation, current problem, simplest useful result, known constraints, confirmed facts, AI inferences, and items to confirm. Never present an inference as fact.

Classify the requested evidence:

- Runtime behavior;
- Contract/interface consistency;
- Governance/process control;
- Artifact presence and quality;
- Mixed, with each criterion labeled.

For a Runtime goal, ask how a real user or operator will demonstrate success. A schema, typecheck, build, document, or screenshot alone is insufficient unless that is itself the requested artifact.

## Readiness Ladder

| State | Required understanding | Next action |
| --- | --- | --- |
| `Concept` | Broad idea or pain | Clarify outcome and beneficiary |
| `Direction` | Outcome and primary use | Propose simplest useful workflow |
| `Ready for Planning` | MVP boundary and success evidence | Classify and size the goal |
| `Ready for Execution` | Scope, acceptance, constraints, and authority | Dispatch one Packet |
| `Owner Decision Required` | Consequential choice cannot be inferred | Consolidate options and stop |

Do not block on reversible uncertainty. Record the assumption and choose the safest low-cost default.

## Output

Use `{baseDir}/templates/en/INTENT_BRIEF.md`. Keep it in chat unless planning begins, the user asks to persist it, or another agent needs a durable handoff. End with one recommended action, why it is first, and the evidence it should produce.
