## Description:

A-Share millisecond-level market data watcher using Tencent direct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch A-Share quote snapshots and evaluate market movement signals such as convertible-bond linkage and ETF premium conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence identifies this as a financial market tool with unclear scope and unsafe local notification code.

Mitigation: Review the skill carefully before installation, do not run the daemon with elevated privileges, and avoid relying on alerts for real trades without independent verification.

Risk: The skill uses unauthenticated market-data transport and has background monitoring behavior.

Mitigation: Prefer a version that uses authenticated market-data transport and documents all modes, data sources, and trading-hours behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenswj/skills/ashare-fast-watcher)
- [Tencent direct market data endpoint](http://qt.gtimg.cn/q={codes})

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market signals and alerts should be independently verified before trading decisions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
