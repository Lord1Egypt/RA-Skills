## Description:

Lightweight runtime tool-policy enforcement: detects risky exec/shell patterns and enforces simple tool-usage limits without modifying core systems. Use when auditing recent tool usage and enforcing exec/shell policy before evolution cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can audit recent local session artifacts for risky exec and shell usage, elevated intent, repeated execution patterns, and tool-usage limits. They can use the findings to review policy and generate a local JSON report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was benign but medium-confidence, and some components were only partially scanned, so the review may be incomplete.

Mitigation: Review the skill and unresolved references before installation, and install only if comfortable with that uncertainty.

Risk: The report command writes a JSON file locally and can create its parent directory.

Mitigation: Choose and review the report path before running the report command.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/147258xuan/skills/exec-policy-enforcer)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain-text audit summary and local JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits local session artifacts; the JSON report is written to a local path.]

## Skill Version(s):

0.1.0 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
