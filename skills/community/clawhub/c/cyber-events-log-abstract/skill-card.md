## Description:

Generates concise security-event summary reports from XDR aggregate event statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoweijie](https://clawhub.ai/user/haoweijie)

### License/Terms of Use:

MIT-0

## Use Case:

Security operations teams and developers use this skill to query authorized XDR event aggregates over a selected time window and generate a concise incident summary report covering trends, peak periods, source and victim IPs, high-risk events, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an embedded XDR API key.

Mitigation: Revoke the published key and require users to supply secrets through a protected configuration or secret store.

Risk: The security evidence reports disabled TLS verification.

Mitigation: Enable certificate verification and require an authorized, configurable XDR endpoint before use.

Risk: The security evidence reports local storage of sensitive raw event data.

Mitigation: Disable raw-data retention by default or document retention, access controls, and cleanup requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoweijie/skills/cyber-events-log-abstract)

## Skill Output:

**Output Type(s):** [markdown, text, files, shell commands, guidance]

**Output Format:** [Markdown report text with command-line status messages and optional saved files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a day-range parameter and optional report path; may save raw event data locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
