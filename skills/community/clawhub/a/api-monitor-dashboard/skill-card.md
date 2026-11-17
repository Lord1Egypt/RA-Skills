## Description:

Real-time monitoring dashboard for API uptime, response times, error rates, custom health checks, and alert notifications via email or Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations engineers use this skill to set up API endpoint monitoring, inspect uptime and latency, and receive health-related alerting signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard may expose monitoring data over a local web interface without authentication.

Mitigation: Bind the dashboard to 127.0.0.1 or add authentication before using it in a shared or sensitive environment.

Risk: Untrusted endpoint values may be handled unsafely when adding monitored URLs.

Mitigation: Review and fix the jq URL handling before accepting endpoint values from untrusted users.

Risk: Monitoring internal or metadata-service URLs can expose sensitive network information.

Mitigation: Run the skill in a non-sensitive directory and avoid monitoring internal services unless the environment has been reviewed and isolated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/api-monitor-dashboard)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local monitoring files and expose a browser dashboard when the provided shell script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
