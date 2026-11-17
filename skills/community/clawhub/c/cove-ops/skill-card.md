## Description:

Cove platform operations: channel files, cove.md, webhooks, channels, messages, members, reactions, roles, and permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Cove administrators and agent developers use this skill to manage Cove channel files, cove.md context, webhooks, messages, members, reactions, roles, and permissions through documented API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad live administrative API operations can change or delete Cove channels, messages, roles, and permissions.

Mitigation: Install only for trusted Cove administrators, use least-privileged bot tokens, and require human confirmation before delete, role, or permission changes.

Risk: cove.md and channel files are writable channel content and may be injected into agent context.

Mitigation: Treat channel files as untrusted input, review changes before relying on them, and avoid storing secrets or unsafe instructions in cove.md.

Risk: Webhook URLs contain bearer-style tokens that can send messages without an authorization header.

Mitigation: Keep webhook URLs secret, avoid logging them, and rotate any webhook that may have been exposed.

Risk: Local plugin deployment steps can replace OpenClaw plugin code and restart the gateway.

Mitigation: Run local deployment only when intentionally replacing local plugin code, after reviewing the build output and keeping a backup.

## Reference(s):

- [Cove Ops on ClawHub](https://clawhub.ai/kagura-agent/skills/cove-ops)
- [Cove API base URL](https://staging.cove.kagura-agent.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes permission-sensitive operational guidance for Cove administration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
