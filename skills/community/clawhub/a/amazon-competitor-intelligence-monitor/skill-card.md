## Description:

Analyzes defined Amazon competitor sets with ZooData, producing full competitive teardowns or recurring Quick Check monitoring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and agents use this skill to analyze identified Amazon competitors by keyword, ASIN, or brand and to monitor tracked competitors for price, inventory, rating, and listing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ZooData API key can be redirected through ZOODATA_BASE_URL, including to HTTP or localhost according to the security summary.

Mitigation: Leave ZOODATA_BASE_URL unset unless a reviewed ZooData endpoint is required; do not point it at HTTP, localhost, or unofficial hosts.

Risk: The published install command is unpinned.

Mitigation: Prefer a pinned install source or reviewed commit before deployment.

Risk: Scheduled monitoring stores local baseline and history data and consumes API credits on recurring runs.

Mitigation: Enable scheduled monitoring only after explicit confirmation, monitor credit usage, and delete monitor-data when retained state is no longer needed.

Risk: Runs send ASINs, competitor ASINs, keywords, category paths, and marketplace/date/numeric filters to ZooData.

Mitigation: Use the skill only with data that is acceptable to send to ZooData and avoid entering unrelated profile or account details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apiclaw/skills/amazon-competitor-intelligence-monitor)
- [Publisher Profile](https://clawhub.ai/user/apiclaw)
- [ZooData Skills Repository](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData API Field Reference](references/reference.md)
- [ZooData CLI Contract](references/cli-contract.md)
- [ZooData API](https://api.zoodata.ai/openapi/v2)
- [ZooData](https://zoodata.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, structured API provenance, alert summaries, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY and may create local monitor-data state for baselines, history, and alerts.]

## Skill Version(s):

1.1.9 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
