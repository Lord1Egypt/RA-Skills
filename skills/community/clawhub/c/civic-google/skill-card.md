## Description:

Use gog, the Google Workspace CLI, without manual OAuth setup while Civic handles token management automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[civictechuser](https://clawhub.ai/user/civictechuser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Google Workspace tasks through gog while Civic handles OAuth consent, scoped token delivery, and token refresh.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Civic brokers OAuth access to Google Workspace data and the gateway uses a CIVIC_TOKEN environment variable.

Mitigation: Install only when this trust boundary is acceptable, isolate the gateway environment, and avoid exposing environment variables in logs.

Risk: Agents can run gog commands within Google scopes the user approves, including write scopes after consent.

Mitigation: Approve only the least Google scopes needed and review commands before execution where workspace changes could be material.

Risk: The release requires external plugin and gog installations.

Mitigation: Pin or verify the plugin and gog versions before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and CIVIC_TOKEN environment variable; Google authorization may require user consent for each scope.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
