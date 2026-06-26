# Weak-Model Guide
#tags: skills review

## Weak-model cheat sheet
- route first
- for skill topics classify skill
- paste real artifact inline, broadly enough for the exact claim under review
- in `multi`, remember each consultant sees only its own chat; repaste needed context when switching consultants unless that same consultant already saw it in its own continuing chat
- no path-only review
- do not treat `FILE:` labels without body text, shell snippets, literal placeholders like `$(cat ...)`, local paths, filenames, summaries of unseen material, or your own hidden checks as pasted artifact text
- produce `SELF_POSITION` before any consultant call in `api` or `multi`
- do not skip `SYNTHESIS`
- emit the minimum round block first; add extended fields second only when they help
- when extended fields are emitted, put `VALIDATION_STATUS` first
- if accepted fix exists, patch before next review
- if launch transport keeps triggering approval cards for otherwise allowed work, do not claim safeguards were disabled; switch to direct stdin or file redirection when supported and continue inside the same safety boundary
- if continuation is missing, continue
- if response is vague twice, narrow or switch to `analysis-only`
- stop only on explicit convergence

## Minimum viable path
### For skill topics
1. Route.
2. Classify the skill.
3. Paste the real skill text inline.
   - Inline means the transmitted consultant prompt already contains the actual artifact text needed for the exact claim under review.
   - Paths, filenames, `FILE:` labels without body text, shell snippets, literal placeholders like `$(cat ...)`, or summaries of unseen sections are invalid.
   - If the claim depends on local code, tests, checks, or validation output, paste that material too.
4. Produce `SELF_POSITION`.
5. Get critique if the orchestrator mode is not `local`.
6. Produce `SYNTHESIS`.
7. Decide.
8. Patch if accepted.
9. Emit the minimum round block.
10. Continue or stop.

### For non-skill topics
1. Route.
2. Paste the real artifact or context inline.
3. Produce `SELF_POSITION`.
4. Get critique if the orchestrator mode is not `local`.
5. Produce `SYNTHESIS`.
6. Decide.
7. Patch if needed.
8. Emit the minimum round block.
9. Continue or stop.

## Compact consultation forms
Use these when the model is constrained, but keep the same logic.

```text
SELF_POSITION_COMPACT:
- verdict: <...>
- weakness: <...>
- fix: <...>

CONSULTANT_POSITION_COMPACT:
- consultant_verdict: <...>
- strongest_finding: <...>
- proposed_fix: <...>

SYNTHESIS_COMPACT:
- relation: <aligned|partial|divergent>
- decision: <...>
- next_action: <...>
```

Rules:
- compact form is allowed
- skipping self -> consultant -> synthesis is not allowed in `api` or `multi`
- in `local`, use self plus synthesis only
- if consultant input is unavailable after the allowed retry, switch mode or mark the round invalid instead of pretending the consultant step happened
- if consultant extraction fails after the allowed retry and the round downgrades, emit `CONSULTANT_POSITION_STATUS: omitted-invalid` to preserve the contiguous status block invariant

## Design rules
- keep the visible runtime short
- flatten branch depth
- name the mode early
- avoid hidden cross-references for core enums and minimum fields
- keep stop rules short and explicit
- force a structured round block
- do not rely on vague prose as a success signal
- treat `analysis-only` as a valid mode, not a failure state
- skip the method on trivial low-risk reversible work
- when self-review or native-domain-adjacent review is active, preserve a real outside-self weakness and a real smallest stronger patch even in compact form

## Common failure patterns
- too many nested sections
- implicit state tracking
- long detours before the first action
- path-only review
- placeholder-only or file-label-only artifact prompts
- omitted self position in consultant-bearing modes
- omitted synthesis after consultant response
- omitted docs or tests checks for the asked scope
- stopping after the first useful comment
- carrying publish logic into generic review too early

## Full-review fallback
Use the weak-model shortcut when you cannot safely manage the full review flow.

## Safe default
If the skill is ambiguous, choose the smallest safe action that still makes progress and record the choice.
