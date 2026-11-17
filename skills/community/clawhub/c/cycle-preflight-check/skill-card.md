## Description:

Pre-flight checks for evolver cycles to detect likely empty cycles, duplicate genes, and tool bypass patterns before running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before running evolver cycles to identify likely empty cycles, duplicate recent intent and gene pairs, excessive shell or exec usage, uncommitted changes, and missing validation scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports medium confidence, partial inspection, and a permissions-scope issue.

Mitigation: Review the skill's environment access and run it only in a workspace where that access is appropriate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/147258xuan/skills/cycle-preflight-check)
- [Publisher profile: 147258xuan](https://clawhub.ai/user/147258xuan)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Plain text status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PASS or WARN with a one-line actionable hint.]

## Skill Version(s):

0.1.0 (source: package.json and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
