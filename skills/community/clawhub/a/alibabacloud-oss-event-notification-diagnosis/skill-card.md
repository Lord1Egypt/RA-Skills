## Description:

Diagnoses Alibaba Cloud OSS event-notification and upload-callback failures using read-only bucket checks and evidence-based guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to investigate missing OSS event notifications and failed upload callbacks without changing bucket configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostics access OSS bucket configuration metadata using the user's Alibaba Cloud credentials.

Mitigation: Use a least-privilege RAM identity and avoid broad production credentials when possible.

Risk: The workflow may request an aliyun CLI installation or upgrade.

Mitigation: Review and approve any CLI installation or upgrade separately.

Risk: The skill cannot directly confirm dependent-service activation or delivery.

Mitigation: Verify SMQ/MNS or EventBridge status in the relevant console before concluding delivery is working.

## Reference(s):

- [Event notification rules and troubleshooting](references/event-notification-rules.md)
- [Upload callback troubleshooting](references/callback-troubleshooting.md)
- [RAM read-permission guidance](references/ram-policies.md)
- [Alibaba Cloud OSS event notifications](https://help.aliyun.com/zh/oss/user-guide/event-notifications/)
- [Alibaba Cloud OSS upload callbacks](https://help.aliyun.com/zh/oss/developer-reference/callback)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown diagnostic summary and recommended next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports unavailable checks and degraded findings rather than assuming a cause.]

## Skill Version(s):

0.0.1 (source: ClawHub release and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
