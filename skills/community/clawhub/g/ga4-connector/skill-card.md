## Description:

Query Google Analytics 4 (GA4) data through the Google Analytics Data API for trends, countries, sources, pages, and conversion analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanaco666](https://clawhub.ai/user/nanaco666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to set up OAuth access and run GA4 Data API reports inside OpenClaw for traffic, source, page, country, trend, and conversion analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer has a command-execution flaw.

Mitigation: Review or patch the installer before running it, and only run it with a numeric GA4 property ID you control.

Risk: OAuth client and token files are stored persistently under ~/.config/openclaw.

Mitigation: Store the credential files with restrictive permissions and avoid running the skill on shared machines until credential handling is hardened.

Risk: The installer adds Python packages to the user environment without pinned dependency versions.

Mitigation: Prefer a virtual environment or pinned dependencies before installation.

## Reference(s):

- [GA4 Data API OpenClaw setup](references/setup.md)
- [GA4 Connector ClawHub page](https://clawhub.ai/nanaco666/skills/ga4-connector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON query output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [GA4 query output is JSON; pretty-printed JSON is available with the provided command option.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
