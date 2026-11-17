## Description:

Generates an agent deployment kill card with stop conditions, revocation actions, an owner, and recovery conditions, and checks it for missing fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment operators use this skill to prepare and check emergency stop plans before launching agents, especially for sensitive or high-risk work. It checks whether required kill-card fields are present; it does not itself stop a running agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented command flags do not match the bundled script, so an untested deployment check may fail.

Mitigation: Check the actual CLI help and test the intended command before using its exit status as a release gate.

Risk: The declared tool permissions are broader than this local checker needs.

Mitigation: Review and restrict the agent's enabled tools to those needed for local card generation and validation.

Risk: Release license metadata and bundled license descriptions disagree, and the documentation reserves rights.

Mitigation: Confirm the license and its scope before distributing or reusing the code and documentation.

## Reference(s):

- [Agent Kill Switch on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-kill-switch)

## Skill Output:

**Output Type(s):** [JSON configuration, Text validation results]

**Output Format:** [JSON kill card or plain-text/JSON validation result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save a kill card to a file; returns exit status 0 for success, 1 for missing required fields, or 2 for invalid input.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; bundled SKILL.md lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
