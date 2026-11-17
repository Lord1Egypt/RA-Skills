## Description:

Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:


## Use Case:

External developers, product teams, and marketplace analysts use this skill to compare Amazon ASINs for pricing, specifications, review patterns, market positioning, moats, and competitor vulnerabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASINs are sent to BrowserAct for browser automation.

Mitigation: Use the skill only with ASINs you are comfortable sending to BrowserAct.

Risk: API keys may be exposed if passed directly on the command line.

Mitigation: Prefer BROWSERACT_API_KEY via the environment or a protected .env file instead of --api-key.

Risk: Generated reports may contain untrusted marketplace content, especially in CSV output.

Mitigation: Treat generated CSV and report files as untrusted when opening them in spreadsheet or document tools.

Risk: Report files are written to the configured output directory.

Mitigation: Choose the output directory intentionally before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-competitor-analyzer)
- [BrowserAct](https://browseract.com)
- [BrowserAct API settings](https://www.browseract.com/reception/integrations)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [CLI text plus local CSV, Markdown, and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one or more ASINs, a BrowserAct API key, and an output directory for generated reports.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
