## Description:

Guides frontend feature work and behavior-changing bug fixes through failing behavior tests, minimal implementation, and refactoring after tests pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to add observable behavior or fix defects with test-first, red-green-refactor cycles. For behavior-preserving refactoring, they keep existing characterization tests green instead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying test-first behavior changes to styling-only, documentation-only, backend-only, or pure refactoring tasks creates unnecessary or misleading tests.

Mitigation: Use this workflow for observable frontend behavior changes; keep existing tests green for pure refactoring and choose another workflow for unrelated tasks.

Risk: A failing test caused by setup errors or an unrelated defect can misdirect implementation.

Mitigation: Confirm that the test fails for the intended missing behavior before changing code, then rerun it after the minimal fix.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-tdd-workflow)
- [Frontend Craft repository (listed in package metadata; import provenance unavailable)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Tests and minimal implementation code with a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes test commands, covered behavior, and remaining risks.]

## Skill Version(s):

2.9.0 (source: ClawHub release, README.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
