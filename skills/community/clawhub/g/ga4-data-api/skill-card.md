## Description:

Query Google Analytics 4 (GA4) data through the Google Analytics Data API for trends, countries, sources, pages, and conversion analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanaco666](https://clawhub.ai/user/nanaco666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and OpenClaw users use this skill to set up OAuth-based GA4 access and query traffic, country, source, page, trend, and conversion-style reports. It is intended for cases where the user already has or can verify access to the target GA4 property.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer modifies shell startup files to store GA4_PROPERTY_ID.

Mitigation: Review the installer before running it, or set GA4_PROPERTY_ID manually in a controlled environment.

Risk: OAuth client and token files are stored under ~/.config/openclaw.

Mitigation: Restrict permissions on ga4-client.json and ga4-token.json and use only trusted GA4 property IDs.

## Reference(s):

- [GA4 Data API OpenClaw setup](references/setup.md)
- [ClawHub skill page](https://clawhub.ai/nanaco666/skills/ga4-data-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON query output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OAuth credentials and a GA4 property ID supplied by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
