---
name: fec-validation-fix
description: Use when running existing project validation commands and fixing failures after code changes, including lint, type-check, unit/integration test, build, CI, or local script failures. Do not use when the task is to design or author new component/E2E tests; Chinese triggers include validation, check failures, fix failures, CI failures.
---

# Verify and fix

## Purpose

Automatically execute existing verification commands, analyze the reasons for failure and safely repair them to ensure that quality access control meets standards.

## Procedure

1. Identify available commands from package.json or repository documentation.
2. Prioritize execution in the following order:
   - lint
   - type-check
   - unit/integration tests
   - build
3. Read the failure output carefully.
4. Group errors by file, error type and dependency, prioritizing root causes that block subsequent diagnosis.
5. Fix one type of problem at a time and display or log critical error context.
6. After each critical repair, re-execute the affected command to confirm whether the error is reduced.
7. If the same error still fails to be repaired three times in a row, stop expanding changes and report blocking.
8. Finally, press `Expected Output` to summarize the execution results, repair content and remaining risks.

## Failure Triage

- Fix the earliest errors that will cascade first, such as missing types, import failures, and configuration parsing failures.
- Differentiate between real product bugs, test environment issues, snapshot drift, dependency version changes and flaky.
- Log Node version, package manager, environment variables, path case, and working directory differences for CI-specific failures.
- When fixing tests, give priority to fixing product code or testing waiting methods, instead of deleting assertions to cover up real regressions.

## Constraints

- Do not blindly turn off rules to eliminate errors
- Don't compromise type safety to pass checks unless there is a clear reason to do so
- Don’t rewrite irrelevant modules just because a nearby test fails
- Do not modify multiple irrelevant root causes at once
- Don't remove failing tests to make validation pass
- Don't just run a fragment of the failed command and claim that the overall validation passed

## Detailed reference

When writing a verification fix report, load [references/report-template.md](references/report-template.md).

## Expected Output

- All verification commands such as lint/type-check/test/build passed
- Failed items have been fixed or given clear reasons and follow-up actions
- The fix report is saved as `reports/validation-fix-YYYY-MM-DD-HHmmss.md`
