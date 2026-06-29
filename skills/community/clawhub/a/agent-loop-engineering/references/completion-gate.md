# Completion Gate

Use this before declaring a loop or task complete.

## Completion States

### Done

Use `Done` only when:

- Every must-pass success criterion in `Docs/ACCEPTANCE.md` is satisfied.
- The implementation remains inside `Docs/TARGET.md` scope.
- Automatic verification passed, such as tests, typecheck, build, lint, or syntax checks.
- Functional verification passed, such as a manual flow, sample input/output, screenshot, API call, or acceptance scenario.
- Remaining risks are minor and do not affect the stated target.

### Done with Risk

Use `Done with Risk` when:

- The core goal appears satisfied.
- At least one important check, environment path, edge case, or manual confirmation is missing.
- The missing evidence is clearly recorded.
- The next human or agent can reproduce what was verified and what remains uncertain.

### Blocked

Use `Blocked` when:

- Completion cannot be judged from available evidence.
- A required permission, credential, account, environment, production resource, or human decision is missing.
- A hard stop rule is triggered.
- The loop cannot safely continue within budget.

### Continue

Use `Continue` when:

- The target is clear.
- No hard stop is triggered.
- Budget remains.
- One concrete next action exists.

## Evidence Classes

Prefer at least two evidence classes for `Done`:

- Automatic verification: tests, typecheck, build, lint, syntax validation.
- Functional verification: sample run, UI flow, API request, screenshot, fixture, acceptance scenario.
- Code review evidence: diff review, risk review, dead-code/security review.
- Documentation/handoff evidence: updated usage notes, status, evaluation, or handoff.

`Done` requires automatic verification plus functional verification unless the project explicitly has no runnable artifact. If no runnable artifact exists, record why and use review/documentation evidence instead.

## Core Verification Selection

Use `Docs/LOOP_CONFIG.md` -> `core_verification` when present. If it is missing:

1. Use `verification_commands.test`.
2. If no test command exists, use `typecheck`.
3. If no typecheck command exists, use `build`.
4. If no build command exists, use `lint`.
5. If no runnable command exists, use `review` and record `No runnable artifact` in `Docs/EVALUATION.md`.

Core verification failure counts toward `max_consecutive_failures` unless the loop produced a configured progress signal.

Only `core_verification` failures consume `max_consecutive_failures`. Non-core failures, such as lint failing while tests pass, must be recorded as risks or missing evidence but do not consume this specific budget unless the project config says so.

## Conflicting Evidence

When automatic verification and functional verification disagree:

- Functional verification failure blocks `Done`, even if all automatic checks pass.
- Automatic verification failure blocks `Done`, even if a manual flow appears to work.
- If the next fix is clear and budget remains, use `Continue`.
- If the core goal appears satisfied but the failing evidence is outside the current target or requires manual confirmation, use `Done with Risk`.
- If the conflict prevents judging completion, use `Blocked`.

Record the conflict in `Docs/EVALUATION.md` with the command or scenario, observed result, and affected acceptance item.

## Functional Verification By Project Type

| Project type | Functional evidence |
| --- | --- |
| Frontend app | Render the changed page or component, exercise the main interaction, and capture screenshot, DOM assertion, or browser evidence when possible. Minimum: route/component, action, assertion/result. |
| API service | Run a request against the changed endpoint, a curl/httpie sample, or a representative integration test with response snippet. Minimum: method/path, request class, status/result snippet, assertion. |
| CLI | Run `--help` plus one core command with sample input and expected output. Minimum: command, input, exit status, expected output snippet. |
| Library or SDK | Import the package and call the changed public function in a test or small sample. |
| Data pipeline | Run a dry-run, sample transform, fixture-based job, or query preview. |
| Infrastructure/config | Run plan, validate, dry-run, or static policy check. |
| Documentation-only or skill-only project | Run structural validation and review the rendered or linked documentation paths. |
| Headless runner with no UI access | Use test-id assertions, DOM snapshots, API samples, fixture runs, or mark `Done with Risk` with manual confirmation listed. |

For feature work, prefer at least one positive scenario and one negative or boundary scenario when that can be done without exceeding scope. If only one scenario is practical, record why.

## No Runnable Artifact

A project has no runnable artifact only when it is purely documentation, prompt/skill text, policy, configuration guidance, or static reference material. Record this in `Docs/EVALUATION.md` and replace functional verification with review/documentation evidence.

For this case, `review` means structural validation plus documented review evidence, such as required files present, schema/frontmatter valid, internal links or references checked, examples aligned with the protocol, and no sensitive content detected.

## Evaluation Template

```markdown
## Completion Gate

- State: Done / Done with Risk / Blocked / Continue
- Target alignment:
- Success criteria:
- Acceptance evidence updated:
- Non-goals preserved:
- Automatic verification:
- Functional verification:
- Risks:
- Missing evidence:
- Next action:
```
