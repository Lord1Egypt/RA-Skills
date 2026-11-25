## Description:

Retrieves public Douyin video, creator, comment, and trending data as structured JSON for social media content and performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Social media operators, marketers, researchers, and analysts can search public Douyin videos and creators, inspect post details and comments, and retrieve trending topics. They can use the structured results to compare content performance, identify topics, and prepare audience or sentiment analyses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence with partial coverage (31 of 53 components fully inspected) and flags keyword-based Douyin account discovery as a concern.

Mitigation: Use creator discovery only when it is part of the intended task, keep searches focused on public accounts and relevant terms, and review the partially analyzed material if stronger assurance is needed.

Risk: Queries send keywords and Douyin links or IDs to the GUAIKEI third-party API.

Mitigation: Review query terms and identifiers before running a command, and avoid sending confidential or sensitive information.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-record-organizer)
- [GUAIKEI service and API access](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [Search options](artifact/references/options.md)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Customer acquisition guide](artifact/references/customer-acquisition.md)
- [Error handling guide](artifact/references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON records with optional concise analysis or guidance based on the retrieved data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Douyin data; available result volume depends on the query and API plan. Requires a GUAIKEI API token.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
