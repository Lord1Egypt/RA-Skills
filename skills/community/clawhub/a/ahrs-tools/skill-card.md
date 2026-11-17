## Description:

AHRS quaternion decomposition and roll/pitch compensation utilities for agents helping with pywayne.ahrs.tools usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to get concise guidance and Python examples for decomposing AHRS quaternions into rotation, heading, and inclination angles and compensating roll and pitch with pywayne.ahrs.tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python examples depend on numpy, qmt, and pywayne being installed in the user's environment.

Mitigation: Install dependencies only from trusted sources and verify package provenance before running examples.

Risk: Quaternion math guidance can produce incorrect orientation results if inputs use an unexpected component order or convention.

Mitigation: Confirm the input quaternion order and validate results against known AHRS test cases before relying on outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/ahrs-tools)
- [Publisher profile](https://clawhub.ai/user/wangyendt)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only guidance; no hidden execution, persistence, data access, or credential handling reported by security evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
