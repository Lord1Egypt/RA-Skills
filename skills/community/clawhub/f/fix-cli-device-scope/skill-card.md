## Description:

Helps diagnose and repair OpenClaw CLI device scope issues that cause subagent, spawn, or cron operations to fail with pairing required errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whhh1994](https://clawhub.ai/user/whhh1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose an OpenClaw CLI device with insufficient permissions and apply a local recovery workflow when pairing-required errors block spawn or cron operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair workflow can grant broad admin-level OpenClaw device permissions and rewrite local authentication files.

Mitigation: Prefer official pairing or admin approval flows when available, verify the target device and requested scopes, keep backups, use dry-run previews, and avoid --force unless automation explicitly requires it.

Risk: The workflow may include highly sensitive scopes such as approval, pairing, and operator.talk.secrets permissions.

Mitigation: Treat requested scopes as sensitive, grant only to the intended CLI device, and review the changed local trust and token files before restarting the gateway.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local diagnostics, dry-run previews, configuration rewrites, and verification guidance for OpenClaw CLI device scope repair.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
