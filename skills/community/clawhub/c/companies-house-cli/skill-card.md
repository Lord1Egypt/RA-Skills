## Description:

UK Companies House CLI for searching companies, profiles, officers, filings, PSC, charges, insolvency, and producing agent-friendly JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shan8851](https://clawhub.ai/user/shan8851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and analysts use this skill to install and operate the ch CLI for UK Companies House lookups, including company search, profiles, officers, filings, PSC records, charges, and insolvency checks. It is useful when an agent needs stable text or JSON envelopes for downstream parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a third-party npm CLI before use.

Mitigation: Pin and review the @shan8851/companies-house-cli package version before installing it in environments that allow third-party packages.

Risk: The skill requires COMPANIES_HOUSE_API_KEY for live API calls.

Mitigation: Scope the key to the execution environment, keep any .env file out of version control, and rotate the key if exposure is suspected.

Risk: Broad person searches can fan out into multiple appointment requests and increase API usage.

Mitigation: Use --match-limit for broad names and avoid combining pagination choices that the CLI marks as incompatible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shan8851/skills/companies-house-cli)
- [Skill homepage](https://ch-cli.xyz)
- [Companies House developer portal](https://developer.company-information.service.gov.uk/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the CLI itself returns text or JSON envelopes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ch binary and COMPANIES_HOUSE_API_KEY for live Companies House API calls.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
