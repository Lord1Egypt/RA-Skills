## Description:

Clawhub Mirror helps agents select and configure ClawHub mirror registries, prioritizing China-accessible mirrors and prompting for VPN use when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixiaohe](https://clawhub.ai/user/xixiaohe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users can use this skill to configure faster or more reachable ClawHub registry endpoints for skill installation and updates. It is most relevant in network environments where the default ClawHub endpoints are slow, blocked, or require VPN access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent mirror configuration can redirect future ClawHub installs to alternate registries.

Mitigation: Use only trusted mirror operators, prefer session-only environment variables, and confirm ClawHub package signatures or hashes before relying on redirected installs.

Risk: Generated loader scripts can preserve mirror choices across future shell sessions.

Mitigation: Review local files under the ClawHub configuration directory before sourcing or adding loaders to a shell profile.

Risk: Reachability and latency checks can select an endpoint for convenience without proving that the endpoint is trustworthy.

Mitigation: Pin approved registries in managed environments and manually inspect the selected mirror before installing or updating skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixiaohe/skills/clawhub-mirror)
- [Publisher profile](https://clawhub.ai/user/xixiaohe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell or PowerShell commands, JSON configuration examples, and executable Python helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local ClawHub mirror configuration and loader scripts when its helper scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
