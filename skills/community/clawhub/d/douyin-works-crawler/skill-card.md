## Description:

Retrieves Douyin account profile data and up to 50 recent works by nickname or Douyin ID, including engagement metrics, direct links, and a brief top-performing content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as brand marketers, MCN operators, Douyin creators, and data analysts use this skill to retrieve recent Douyin account works, compare engagement, and support content performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin account identifiers to RedFox and returns collected account and work data.

Mitigation: Install only when that data transfer and downstream use are lawful, appropriate for the use case, and consistent with applicable platform terms.

Risk: Security evidence reports that the script prints an API-key prefix, which can expose credential material in shared logs.

Mitigation: Avoid sharing execution logs and remove API-key prefix printing before deployment in shared or monitored environments.

Risk: Security evidence reports an unrelated RedFox sales link in generated reports.

Mitigation: Review generated output before distribution and remove sales-link content when it is not appropriate for the audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-works-crawler)
- [Core workflow reference](references/core_workflow.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include account fields, up to 50 recent works, engagement metrics, direct links when available, and TOP 3 engagement analysis.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
