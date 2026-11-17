## Description:

F-AI 金融数据 helps agents query Finloop market-data APIs for real-time and historical prices, fund and bond data, and company fundamentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czzlegend](https://clawhub.ai/user/czzlegend)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer market-data and fundamental-analysis questions by issuing direct HTTP POST requests to Finloop endpoints for stocks, indices, funds, bonds, and companies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer behavior can write outside the intended skills folder.

Mitigation: Install only in an expected workspace and review the target .agents/skills path before allowing overwrite.

Risk: The install command runs an unpinned npm package.

Mitigation: Use a pinned, trusted package version when installing.

Risk: API calls go to Finloop's UAT service.

Mitigation: Do not include confidential portfolio, account, or personal data unless that service has been approved for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/czzlegend/skills/finloop-mktdata-skills)
- [Finloop market data API reference](artifact/.agents/skills/finloop-mktdata-skill/references/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and response-field interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include direct fetch, axios, or curl requests to Finloop API endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
