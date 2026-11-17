## Description:

OpenClaw Cloudways integration reference and workflow guide for creating, editing, reviewing, debugging, and extending Cloudways account auth, inventory, vault-backed server/app credentials, WordPress review flows, DB Manager access, guarded SQL execution, and the Control UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain OpenClaw's built-in Cloudways integration for Cloudways-hosted WordPress review and maintenance workflows, including account setup, inventory loading, secure credential handling, and guarded database actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports workflows that handle Cloudways, SSH, WordPress, and database credentials.

Mitigation: Install only for managing Cloudways-hosted WordPress sites through OpenClaw, treat configured credentials as production-sensitive, and use least-privilege access where possible.

Risk: Database actions can affect production WordPress data when writes are confirmed.

Mitigation: Verify the selected app and server before running database actions, prefer read-only or dry-run paths first, and rely on the documented confirmation and audit logging for writes.

Risk: Live Cloudways, SSH, and DB Manager operations can fail because of authentication, network, or remote platform changes.

Mitigation: Validate Cloudways account credentials, test SSH and DB access before maintenance work, and confirm the selected application context before acting.

## Reference(s):

- [Cloudways Integration on ClawHub](https://clawhub.ai/maverick-software/skills/cloudways-integration)
- [Implementation Reference](artifact/references/implementation.md)
- [Gateway Methods Reference](artifact/references/request-methods.md)
- [Cloudways API Notes](artifact/references/cloudways-api-notes.md)
- [UI Design Reference](artifact/references/ui-design.md)
- [Status Response Example](artifact/assets/examples/cloudways-status-response.json)
- [Metadata Response Example](artifact/assets/examples/cloudways-metadata-response.json)
- [Read Query Response Example](artifact/assets/examples/cloudways-read-query-response.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code and configuration references plus JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guarded operational steps for Cloudways credentials, SSH and DB checks, and SQL workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
