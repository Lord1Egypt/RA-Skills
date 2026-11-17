## Description:

Query public skills published by a ClawHub user from the real public API. Returns skill list, versions, timestamps, and metadata. Does not fabricate installs, downloads, ratings, or review counts when the public API does not expose them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list public ClawHub skills for a user, inspect versions and timestamps, and export available public package metadata without inventing unavailable public metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to clawhub.ai to retrieve public package metadata.

Mitigation: Use it only in environments where outbound access to clawhub.ai is permitted and where public metadata queries are appropriate.

Risk: CSV exports can contain untrusted public text that spreadsheet tools may interpret as formulas.

Mitigation: Treat exported CSV files as untrusted data and inspect them as plain text or disable spreadsheet formula execution before opening.

Risk: The public API used by the skill does not expose installs, downloads, ratings, or review counts.

Mitigation: Return those fields as unavailable or null instead of estimating or fabricating metrics.

## Reference(s):

- [ClawHub Skill Monitor package page](https://clawhub.ai/harrylabsj/skills/clawhub-skill-monitor)
- [ClawHub public packages API](https://clawhub.ai/api/v1/packages?family=skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and text, JSON, or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can scan paginated public package results and optionally write a CSV export when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
