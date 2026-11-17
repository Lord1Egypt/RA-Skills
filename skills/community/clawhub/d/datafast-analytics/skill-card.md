## Description:

Query DataFast website analytics and visitor data via the DataFast API for metrics, time series, realtime stats, breakdowns, visitor details, and goal/payment management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennyqp](https://clawhub.ai/user/bennyqp)

### License/Terms of Use:


## Use Case:

Developers and website operators use this skill to query DataFast analytics, inspect visitor activity, summarize realtime or historical metrics, and manage goals or payments through the DataFast API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete DataFast goals or payments.

Mitigation: Require explicit human approval for every delete request, including exact filters, time range, and final URL without the API key.

Risk: The skill uses a DataFast API key that may expose analytics and visitor details.

Mitigation: Use the least-privilege or read-only key available, store it with owner-only permissions, and avoid pasting the secret into chat prompts.

Risk: Broad time ranges or vague delete scopes could affect more records than intended.

Mitigation: Confirm destructive scope in plain language and require additional confirmation for all-time deletion requests.

## Reference(s):

- [DataFast homepage](https://datafa.st)
- [DataFast API base URL](https://datafa.st/api/v1/)
- [ClawHub skill page](https://clawhub.ai/bennyqp/skills/datafast-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pagination details, totals, conversion or revenue metrics, and confirmation prompts for destructive actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
