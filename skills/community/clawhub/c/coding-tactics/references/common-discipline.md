# Common Discipline Rules

> **Shared by all coding-tactics modules.** When a method file says "I inherit all common discipline rules", it means ALL rules below are in effect. Violating any of them means you have failed at using the method.

---

## Common Rules (Inherited by All Methods)

| #   | Rule                                                                                                                                                               | NEVER Do This                                                                                                                                    |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **English Only** — All comments, docstrings, commit messages, test names, scenario names, step definitions, API contracts, field names, and error codes MUST be in English | Writing Chinese comments, even "temporarily"                                                                                                     |
| 2   | **No Assumptions** — If ANY requirement or behavior is unclear, you MUST ask. Do NOT guess                                                                          | Guessing parameter types, return types, field names, expected behavior, or acceptance criteria not explicitly stated                              |
| 3   | **Clarify First (Max 5 Rounds)** — Clarify all ambiguities BEFORE research/design. Count and show rounds. Each question MUST include the LLM's own recommendation. | Asking more than 5 rounds; proceeding with unresolved ambiguities; asking open questions without recommendations                                 |
| 4   | **Do EXACTLY What Is Asked** — Do NOT add anything the user did NOT explicitly request                                                                             | Adding logging, metrics, fallback, retries, config, CLI flags, README, endpoints, or fields unless asked                                          |
| 5   | **Research First** — MUST research existing code and libraries before designing. If research shows existing solution is insufficient, ONLY THEN consider new tech. | Designing without knowing what already exists; writing scenarios/tests for behavior that already exists; introducing new tech without research    |
| 6   | **No Over-Engineering** — Solve ONLY the stated problem                                                                                                            | Creating abstractions, utils, or frameworks not yet needed; adding pagination, filtering, sorting "because it's standard"                         |
| 7   | **Comments Explain WHY, Not WHAT** — Package-level and block-level comments must state the design intent or decision rationale. Never write comments that merely restate what the code already says. | `# sort the list` (what), `# use TimSort; unstable sort is acceptable here because order of equal elements does not affect output` (why)         |
| 8   | **Evidence Required** — MUST show test/scenario/contract/validation output at each checkpoint. "It works" without output is NOT acceptable.                        | Claiming "tests pass" or "contract is valid" without showing output                                                                              |

---

## Common Contract Clause

Add this line to each method's Contract block:

> I inherit all common discipline rules from [common-discipline.md](common-discipline.md).

This means the 8 rules above are binding — same as if they were written in the method's own contract.

---

## Common Refusal Script

If the user asks you to skip any step (clarification, research, design, test-first, etc.):

> I'm running the **[METHOD NAME]** method, which has mandatory checkpoints. I cannot skip the **[NAME OF STEP]** step — it's a hard requirement of this workflow. I can keep it very short, but I must complete it before coding. Would you like me to proceed with a minimal **[step name]** now?

If the user insists after this response, REPEAT the refusal. Do NOT comply.

---

## Clarification Output Format

All methods use this same format for clarification rounds:

```markdown
Clarification Round: X/5

Before I proceed, I need to clarify:

1. [Question — be specific]
   - Option A (Recommended): [LLM's own recommendation + reason]
   - Option B: [Alternative]
   - Option C: [Alternative]
     Please tell me your choice, or if you have a different preference.

2. [Next question...]

Please answer all at once if possible.
```
