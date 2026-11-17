## Description:

Automates HTML form creation from roadflow.rf_form using similarity matching, with support for client validation, multi-step wizards, and conditional fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericyang1234](https://clawhub.ai/user/ericyang1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate HTML forms, validation behavior, wizard flows, and related form configuration from field definitions, JSON schema, or similar RoadFlow form records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release publishes PostgreSQL credentials for a RoadFlow database.

Mitigation: Treat the published password as compromised, rotate it, and use dedicated least-privilege credentials from a secret manager or environment variables.

Risk: The skill describes creating new records in roadflow.rf_form without clear safeguards.

Mitigation: Require a dry run, explicit confirmation, and review of generated form content before any database write.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericyang1234/skills/form-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown or text containing HTML, JavaScript, JSON configuration, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include similarity match summaries, generated form markup, field JSON, validation code, and database write guidance.]

## Skill Version(s):

2.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
