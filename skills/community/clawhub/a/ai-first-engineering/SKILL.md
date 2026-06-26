---
name: ai-first-engineering
description: "Engineering operating model for teams shipping with AI-assisted code generation. Process shifts, architecture requirements, code review and testing standards. Trigger phrases: ai-first engineering, ai-assisted teams, agent code generation, ai team process, shared responsibility review."
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"bins":[],"env":[]},"os":["linux","darwin","win32"]}}
---

# AI-First Engineering

Engineering operating model for teams where AI agents generate a large share of implementation output. Adapted from everything-claude-code by @affaan-m (MIT).

## Quick Start

1. **Invest in planning quality** — ambiguous specs cause AI-generated code to fail; write clear acceptance criteria first
2. **Raise eval coverage** — AI code requires higher test standards; regression coverage mandatory for touched domains
3. **Shift review focus** — review for behavior, security, data integrity, failure handling; let automation handle style
4. **Design agent-friendly architecture** — explicit boundaries, stable contracts, typed interfaces, deterministic tests
5. **Evaluate hiring signals** — decomposition skill, measurable criteria definition, prompt quality, risk control discipline

## Key Concepts

- **Planning > Speed:** Clear specs + good evals trump fast typing. AI can implement fast; humans must specify clearly.
- **Automation is the baseline:** Style, formatting, lint issues are solved by automation, not review.
- **Architecture matters more:** Implicit conventions break AI systems; use explicit boundaries and typed interfaces.
- **Test coverage is non-negotiable:** Generated code needs regression coverage for every touched domain.
- **Shared responsibility:** AI generates; human reviews for risk (security, data integrity, rollout safety); human refines when needed.

## Common Usage

**Code review in AI-first teams — focus on:**

```text
Behavior regressions: Did the change break existing functionality?
Security assumptions: Input validation, permission checks, sensitive data handling
Data integrity: Constraints, rollback safety, concurrent access
Failure handling: Network calls, database errors, timeouts, degraded modes
Rollout safety: Feature flags, backward compatibility, canary deploy strategy
```

**Architecture for AI teams:**

- Explicit boundaries between modules (not implicit conventions)
- Stable contracts (typed interfaces, documented behavior)
- Deterministic tests (no flaky tests — AI can't debug intermittent failures)
- Clear error paths (AI struggles with ambiguous error handling)

**Testing standard raise:**

- Regression coverage for every touched domain (required, not optional)
- Explicit edge-case assertions (AI may miss corner cases)
- Integration checks for interface boundaries (behavior across module lines)

## Hiring Signals for AI-First Engineers

**Strong signals:**

- Decomposes ambiguous work cleanly → clear, testable units
- Defines measurable acceptance criteria → no scope creep, clear done condition
- Produces high-signal prompts and evals → AI generates better code from better specs
- Enforces risk controls under delivery pressure → doesn't skip security or testing for speed

**Weak signals:**

- "Move fast and break things" mindset
- Writing code without clear specs or acceptance criteria
- Skipping regression tests to save time
- Vague PR descriptions ("fixed bugs," "refactored stuff")

## References

- `references/process-shifts.md` — detailed planning, evals, review guidance
- `references/architecture-guide.md` — designing systems for AI code generation
- `references/testing-standards.md` — regression coverage, edge-case testing, integration checks
