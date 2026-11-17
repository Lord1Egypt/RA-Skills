## Description:

DataClaw Setup guides users through installing and configuring DataClaw for OpenClaw while clarifying that the actual access-point skill is installed later from the DataClaw UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddanieli](https://clawhub.ai/user/ddanieli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to understand DataClaw setup prerequisites, configure a datasource and access point in the local DataClaw UI, and know when to install the generated access-point skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated DataClaw access-point skill could expose broader database access than intended if configured with excessive permissions.

Mitigation: Configure only the database permissions needed for the intended workflow and prefer approved-query access when available.

Risk: Raw SQL, write, or execute permissions can expose or modify data if enabled without review.

Mitigation: Enable raw query, write, or execute permissions only when required, and confirm the generated access-point skill exposes the expected capabilities before use.

Risk: Users may assume this setup guide provisions an OpenClaw-ready DataClaw connection by itself.

Mitigation: Complete DataClaw installation, datasource setup, access-point configuration, and the DataClaw UI's Install as a Skill step before attempting to use a specific access point.

## Reference(s):

- [DataClaw website](https://dataclaw.sh)
- [DataClaw GitHub repository](https://github.com/ekaya-inc/dataclaw)
- [ClawHub skill listing](https://clawhub.ai/ddanieli/skills/dataclaw-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline setup commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance only; it does not create a DataClaw connection or install the generated access-point skill.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
