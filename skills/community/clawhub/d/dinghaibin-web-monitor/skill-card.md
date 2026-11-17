## Description:

Monitor web pages for content changes with CSS selector targeting, change detection via hashing, and notification integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use Web Monitor to track specific web page content such as prices, listings, and availability, compare snapshots, and trigger notifications when changes are detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS results are unauthenticated because the monitor disables TLS certificate verification.

Mitigation: Fix TLS verification before relying on sensitive HTTPS monitoring, or restrict monitored URLs to sources where this risk is accepted.

Risk: Notification hooks can run unrestricted local shell commands when a page changes.

Mitigation: Use fixed, reviewed notification commands, avoid untrusted or generated input in --notify, and run the monitor as a least-privileged account.

Risk: Watch mode can repeatedly fetch URLs and execute notification commands.

Mitigation: Use approved URLs, set conservative intervals, and avoid running continuous monitors with privileged accounts.

## Reference(s):

- [Web Monitor Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/dinghaibin-web-monitor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text or JSON output with command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local state files and optionally invoke a notification command when a monitored page changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
