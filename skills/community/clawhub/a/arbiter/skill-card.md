## Description:

Push decisions to Arbiter Zebu for async human review when an agent needs human input on plans, architectural choices, or approval before proceeding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5hanth](https://clawhub.ai/user/5hanth)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to submit structured decisions for asynchronous human review, then check status or retrieve completed answers before continuing blocked work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local queue handling can write or expose decision files more broadly than users are told.

Mitigation: Review before installing, use only on a trusted single-user machine, and fix path validation, ownership checks, serialization handling, and file permissions before broader deployment.

Risk: Decision requests may contain secrets, personal data, regulated data, or sensitive internal plans.

Mitigation: Do not send secrets, credentials, personal data, regulated data, or sensitive internal plans through this skill.

## Reference(s):

- [ClawHub Arbiter Skill](https://clawhub.ai/5hanth/skills/arbiter)
- [Arbiter Zebu Bot](https://github.com/5hanth/arbiter-zebu)
- [Arbiter Zebu Architecture](https://github.com/5hanth/arbiter-zebu/blob/main/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON CLI arguments and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local decision queue files under the user's Arbiter directory.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
