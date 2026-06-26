# 9 Dimensions of Intent

Extract only the dimensions needed to make the brief executable. Do not turn this into an interview script when context is already clear.

## 1. Task

What should the agent do?

- One verb, one outcome
- Split unrelated tasks into separate briefs
- Prefer "fix X" / "implement Y" / "review Z" over vague "work on"

## 2. Input

What does the agent need to start?

- Repo, files, URLs, datasets, credentials, or screenshots
- Runtime/host if relevant
- Branch, directory, service, or environment

Avoid vague location text like "in the repo" when the exact path or branch matters.

## 3. Output

What should exist when the agent is done?

- Files created or changed
- Tests/proof artifacts generated
- Commit, PR, report, or message expected
- Service or data state expected

## 4. Constraints

What must not break?

- Existing behaviours
- Files, data, credentials, or generated assets that must not be touched
- Backwards compatibility or performance limits
- Security/privacy boundaries

## 5. Context

What does the agent need to understand about why this task exists?

Keep it short. Include only context that changes the work.

## 6. Audience / Role

Who is the brief for?

- Builder / implementer
- Reviewer / verifier
- Researcher
- Cron or scheduled agent
- Human operator

Role determines autonomy, tool expectations, and output shape.

## 7. Prior Context

What should the agent read first?

- Specs, issue links, previous verdicts, relevant docs
- Existing implementation patterns
- Prior decisions or non-goals

## 8. Success Criteria

How does everyone know it is done?

- Use explicit AC1, AC2, AC3 where possible
- Each AC must be testable by a fresh verifier
- Include the exact verification command or manual check when known

If you cannot write a testable AC, the task is under-defined.

## 9. Examples

What examples clarify the intended result?

- Before/after screenshots
- Expected output format
- Similar accepted implementation
- Known-good command output

## Quick Extraction Prompt

Ask at most three questions in one round:

```text
I can write the brief, but I need three specifics:
1. [missing blocker]
2. [missing blocker]
3. [missing blocker]
```

If more than three answers are missing, ask the three that most affect correctness and note the remaining assumptions in the brief.
