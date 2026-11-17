## Description:

Helps users track Ctrip points, view locally maintained redemption items, and get affordability and redemption recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totti10hj](https://clawhub.ai/user/totti10hj)

### License/Terms of Use:

MIT-0

## Use Case:

External Ctrip users and their agents use this skill to manage point balances, compare redemption options, and maintain a local product list for reward decisions. It is also useful for developers who want command-line helpers for manually updating Ctrip points and redemption data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Ctrip cookie may expose account access if stored or shared insecurely.

Mitigation: Treat the cookie like a password, provide it only on a trusted machine, and prefer manual point updates when account access is unnecessary.

Risk: Automatic monitoring, cron jobs, or Feishu notifications may run or send data to destinations the user has not verified.

Mitigation: Inspect scheduled jobs and notification destinations before enabling monitoring or relying on push notifications.

Risk: The publish command uses the current clawhub package version.

Mitigation: Avoid running the publish command unless the package source is trusted or the package version is pinned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/totti10hj/skills/ctrip-points)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local Ctrip points and product data under ~/.openclaw/data when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
