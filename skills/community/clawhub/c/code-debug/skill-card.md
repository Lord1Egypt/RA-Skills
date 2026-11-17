## Description:

Diagnose failures in the current local codebase and produce the smallest defensible fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose local code errors, crashes, bad output, flaky behavior, and failed tests, then receive a minimal repair path with verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed patches or commands could be incorrect for an important repository even when the skill is narrowly scoped.

Mitigation: Review proposed changes before applying them and run the stated verification steps in the target workspace.

Risk: The workflow is written primarily in Chinese, which may reduce review clarity for users who do not read Chinese.

Mitigation: Use the skill when a Chinese-language debugging workflow is acceptable, or translate key findings before applying fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sf0799/skills/code-debug)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with root-cause analysis, patch or repair guidance, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a minimal reproduction scenario when available.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
