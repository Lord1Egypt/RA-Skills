## Description:

Generates daily, weekly, monthly, and yearly reports of AI-agent usage, including token consumption, estimated costs, task categories, skill use, and automation activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use the skill to review local usage across supported assistants and understand token trends, task mix, skill activity, and automation runs. Cost figures are estimates unless supported by an official usage export, and some data sources provide estimated token counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and collected session details may contain private information if saved or shared.

Mitigation: Get explicit agreement before saving; choose and protect the destination path, then review session-derived content before sharing.

Risk: Enabling LLM task classification sends session-derived text to the selected endpoint.

Mitigation: Keep classification disabled unless the user approves the data transfer and endpoint.

Risk: Reported costs may differ from actual bills.

Mitigation: Verify estimates against the provider's actual usage records or bills.

## Reference(s):

- [Agent Analytics Report on ClawHub](https://clawhub.ai/elisabeth15501/skills/agent-analytics-report)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON]

**Output Format:** [Usage report in Markdown (default), HTML, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily, weekly, monthly, or yearly summaries; includes usage trends and analysis.]

## Skill Version(s):

1.9.13 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
