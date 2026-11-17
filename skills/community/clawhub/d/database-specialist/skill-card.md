## Description:

Database architecture design, SQL optimization, schema review and migration planning, delivered as an AI service after clawtip verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database teams use this skill to request paid, Chinese-language help with database architecture, SQL optimization, schema review, and migration planning after clawtip payment verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because it centers on a paid clawtip flow with broad permissions, external tooling, and weakly protected local order records.

Mitigation: Review the skill carefully before installation, run it in a constrained environment, and use it only with verified clawtip payment tooling.

Risk: Consultation questions may accidentally include database credentials, connection strings, private schema details, or sensitive logs.

Mitigation: Remove secrets and private operational data from the question before creating an order.

Risk: Local order and payment metadata are stored on the user's machine.

Mitigation: Treat local order files as sensitive, restrict access to the user profile, and remove stale records when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinyu12166/skills/database-specialist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires clawtip verification and may create local order metadata before service output is authorized.]

## Skill Version(s):

1.0.28 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
