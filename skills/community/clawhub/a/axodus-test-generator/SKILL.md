---
name: test-generator
description: Generate deterministic unit/integration tests for critical behaviors.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: quality
---

# SKILL: test-generator

## Purpose
Generate deterministic unit/integration tests that protect behavior and enable safe refactors.

## When to Use
- A feature needs coverage.
- A bug fix needs a regression test.
- You want characterization tests before refactoring.

## Inputs
- `target` (required, string): function/module/endpoint/contract behavior to test.
- `test_type` (optional, enum: `unit|integration|e2e`).
- `framework` (optional, string): e.g., `pytest`, `jest`, `vitest`, `foundry`, `hardhat`.
- `constraints` (optional, string[]): no network, deterministic time, limited mocks, etc.

## Steps
1. Identify observable behaviors and edge cases.
2. Decide test boundaries:
   - unit: pure logic
   - integration: DB/service boundary
3. Create fixtures:
   - deterministic data
   - stable clocks/UUIDs (mock only when required)
4. Write tests:
   - happy path
   - failure paths
   - security/validation checks (where applicable)
5. Run tests and iterate until they are stable.

## Validation
- Tests are deterministic (no flaky time/network dependencies).
- Tests fail before the fix (for regressions) and pass after.
- Coverage targets the acceptance criteria, not implementation details.

## Output
- Test files added/changed
- How to run tests
- Notes on fixtures/mocks used

## Safety Rules
- Do not add tests that require real credentials or real external services by default.
- Avoid snapshot tests for highly variable outputs unless stabilized.

## Example
Bug: â€œUser creation accepts invalid email.â€
Output: a failing test asserting `400` on invalid input, then passes after fix.
