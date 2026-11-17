## Description:

Post and manage real-time corkboard pins, lamp cues, deleted-history recovery, and multi-track project pipeline work for Carl's Corkie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zheroz00](https://clawhub.ai/user/zheroz00)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send actionable tasks, alerts, links, briefings, package tracking, media summaries, and multi-track project handoffs to a Carl's Corkie dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer clones and runs code from an upstream GitHub repository with npm and optional PM2 scripts.

Mitigation: Install only after reviewing and trusting the upstream repository and local install script.

Risk: The dashboard exposes API routes protected by a shared bearer token.

Mitigation: Keep the service on localhost or a trusted network, place any public access behind an authenticated proxy, and rotate the token if it is exposed.

Risk: The bearer token is stored in the dashboard .env file.

Mitigation: Treat the .env token as a credential and keep the file private.

## Reference(s):

- [Corkboard Dashboard repository](https://github.com/Grooves-n-Grain/carls-corkie)
- [API Reference](references/api.md)
- [Setup Guide](references/setup.md)
- [Pin Types Reference](references/pin-types.md)
- [ClawHub skill page](https://clawhub.ai/zheroz00/skills/corkboard-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, curl examples, and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local or trusted-network dashboard API using bearer-token authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
