# Brief Formats

Use these as public-safe templates. Replace placeholders with the user's actual environment only when the user has provided it or it is already part of the current task context.

## Builder Brief

```markdown
# Brief: [TASK_ID] - [one-line outcome]

## Confidence Gate

Before starting implementation, ask clarifying questions until you are 95% confident you can complete this task correctly. If you are already 95% confident, state assumptions and proceed.

## Task

[One clear sentence describing what to build or fix.]

## Context

[Only context that changes the implementation. 2-5 sentences.]

## Acceptance Criteria

AC1: [specific, testable condition]
Verify: [command/check]

AC2: [specific, testable condition]
Verify: [command/check]

AC3: [specific, testable condition]
Verify: [command/check]

## Constraints

- [What must not break]
- [Files/data/services that must not be touched]
- [Security/privacy boundaries]

## Non-Goals

- [Explicitly out of scope]

## Read First

- [file/doc/spec/issue link]

## Environment

- Repo/path: [repo/path]
- Branch: [branch]
- Runtime/service: [if relevant]

## Deliver

- Changed files
- Verification output
- Known residual risks
```

## Reviewer / Verifier Brief

```markdown
# Review: [TASK_ID]

## Role

You are the verifier. Do not implement fixes. Verify the acceptance criteria from a fresh session and report evidence.

## Read First

- [spec or brief]
- [existing verdict/problems if any]

## Acceptance Criteria To Verify

AC1: [copy from spec]
AC2: [copy from spec]
AC3: [copy from spec]

## Required Checks

- [test command]
- [manual/browser/API check]
- [regression check]

## Output

Return:
- PASS/FAIL/UNKNOWN for each AC
- Evidence for each verdict
- File/line references for failures when applicable
- Test commands run and exact result
```

## Research Brief

```markdown
# Research: [topic]

## Question

[Specific question to answer.]

## Scope

- Include: [source types, date range, domains, handles]
- Exclude: [known noise]

## Source Quality

- Prefer primary sources.
- Include URLs and publication dates.
- Separate observed facts from inference.
- Flag uncertainty.

## Output

- Short answer
- Evidence table
- Implications
- Open questions
```

## Cron / Scheduled Agent Brief

```markdown
# Scheduled Task: [name]

## Goal

[What should be checked or produced.]

## Steps

1. [Exact action]
2. [Exact action]
3. [Exact action]

## Success Condition

[What normal healthy output means.]

## Alert Condition

Send a message only if:
- [condition]
- [condition]

If everything is healthy, return `NO_REPLY`.

## Output

- Write report to [path] if needed.
- Include exact failure evidence if alerting.
```

## Token Efficiency Checklist

- Can any sentence be removed without changing what the agent does?
- Are paths, branches, commands, and URLs specific where needed?
- Are ACs testable by someone who did not write the code?
- Are constraints and non-goals explicit?
- Are private local assumptions excluded unless required?
- Is the final output shape clear?
