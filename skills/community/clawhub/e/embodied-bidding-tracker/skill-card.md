## Description:

AIRS-具身智能订单信息采集器 organizes public bidding collection, Tianyancha order verification, LLM case extraction, standardized ingestion, and quality review for embodied-intelligence and related industry research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airs-guest](https://clawhub.ai/user/airs-guest)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, analysts, and developers use this skill bundle to confirm company identities, collect public tender evidence, verify third-party order spreadsheets, extract embodied-intelligence case records, and prepare reviewed CSV and Markdown outputs for a research case database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a logged-in Tianyancha browser session through Chrome remote debugging.

Mitigation: Run it only in a trusted local environment with a dedicated browser profile, and close the remote-debugging browser session after collection.

Risk: Selected research records and raw content may be sent to the configured OpenAI-compatible LLM provider.

Mitigation: Use an HTTPS LLM provider you trust, keep config/settings.json private, and avoid processing data that should not leave the local environment.

Risk: Spreadsheet processing depends on xlsx handling that the security evidence flags for known vulnerable behavior.

Mitigation: Upgrade or replace the vulnerable xlsx dependency before processing untrusted spreadsheets, and avoid opening generated spreadsheet outputs with formula execution enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/airs-guest/skills/embodied-bidding-tracker)
- [Project Homepage](https://github.com/airs-guest/airs-embodied-intelligence-research-skills)
- [Tianyancha](https://www.tianyancha.com)
- [Artifact README](artifact/README.md)
- [Root Skill Definition](artifact/SKILL.md)
- [Skill Catalog](artifact/skills/catalog.json)
- [Application Scenario Classification Rules](artifact/应用场景分类规则.md)
- [Embodied Intelligence Company Database Template](artifact/具身智能中游企业数据库.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, plus generated CSV, JSON progress, raw Markdown evidence, and Markdown report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary generated files include company lists, bidding records, raw content, verification reports, extraction results, review sheets, ingestion CSVs, and ingest reports under data/.]

## Skill Version(s):

1.0.9 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
