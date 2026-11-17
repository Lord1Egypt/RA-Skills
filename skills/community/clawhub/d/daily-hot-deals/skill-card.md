## Description:

Generates a concise Chinese-language daily deals report using included sample deal data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and deal-focused operators can use this skill to generate a compact daily hot-deals report for review or sharing. The shipped artifact is best understood as a local report generator with sample data, not as a live aggregation, subscription, scheduling, or WeChat push integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises daily deal aggregation, subscriptions, scheduling, and WeChat push behavior, but the artifact contains a local script with hardcoded sample deals.

Mitigation: Review the artifact before deployment and do not provide WeChat credentials, payment details, or automation access unless a future release clearly implements those flows with user controls.

Risk: Deal prices and availability can be stale or inaccurate, especially when generated from sample data.

Mitigation: Confirm prices and availability with the original merchant before acting on or sharing recommendations.

## Reference(s):

- [Daily Hot Deals on ClawHub](https://clawhub.ai/275254cl-hash/skills/daily-hot-deals)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown-style daily deal report, with optional Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; report contents are generated from bundled sample data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
