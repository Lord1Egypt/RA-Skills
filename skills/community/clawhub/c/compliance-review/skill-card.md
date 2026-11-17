## Description:

Automatically reviews compliance of client claim authorization letters using customized insurer templates and sends review results to Feishu every 30 minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulong423401-coder](https://clawhub.ai/user/liulong423401-coder)

### License/Terms of Use:

MIT

## Use Case:

Insurance operations teams in a controlled Chinese insurance-review environment use this skill to check client claim authorization notices for handwritten signatures and required authorization documents across insurer templates, then send review status to Feishu.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Automated first-run approval can approve review decisions without explicit human confirmation.

Mitigation: Disable first-run auto-approval and require human or administrator approval before review decisions are accepted.

Risk: The configured login endpoint uses HTTP for an insurance-review workflow.

Mitigation: Change the login endpoint to HTTPS before use and verify transport security for all connected systems.

Risk: Feishu notifications may expose sensitive review context if recipients and message contents are not scoped.

Mitigation: Limit notification content and recipients, document the Feishu integration, and confirm no customer personal information is collected or transmitted.

Risk: The package is incomplete as provided because its declared runtime entry point is missing.

Mitigation: Install only after the entry point is supplied, dependencies are pinned with a lockfile, and the complete package is reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liulong423401-coder/skills/compliance-review)
- [Publisher profile](https://clawhub.ai/user/liulong423401-coder)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text review results, Feishu notifications, and JSONL audit log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled every 30 minutes; audit logging is configured with 90-day retention.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
