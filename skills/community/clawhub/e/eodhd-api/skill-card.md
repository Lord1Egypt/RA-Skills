## Description:

Provides tools and workflows to interact with the EODHD (EOD Historical Data) API for financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to configure an EODHD API token, fetch market and financial datasets through the included Python client, and present returned JSON as readable summaries or Markdown tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an EODHD API token and may persist it in config.json.

Mitigation: Use a temporary or restricted token when possible, restrict config.json permissions if persisted, and avoid sharing full error objects because they may include the token.

## Reference(s):

- [EODHD API Documentation](https://eodhd.com/financial-apis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided EODHD API token before API calls can succeed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
