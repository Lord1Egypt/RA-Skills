## Description:

Cloud-native backup and role sharing for AI systems using accountless key-based backup, restore, and sharing flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuchiheng](https://clawhub.ai/user/xuchiheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to have an AI agent back up, restore, and share workspace or role configuration through key-based cloud storage flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give a remote service broad access to workspace and agent-state backup data.

Mitigation: Require HTTPS, an explicit file manifest and allowlist, secret redaction, per-action confirmation, and controls to pause sync or delete remote data before use.

Risk: Restore and role-apply flows can overwrite local configuration from remote ZIP data.

Mitigation: Validate ZIP contents safely, inspect changes before applying them, require user confirmation, and keep a local backup or stash before overwrite.

Risk: Keys act as the sole credential and are described as permanent.

Mitigation: Treat keys as secrets and require revocable or expiring keys for production use.

## Reference(s):

- [Dead or Clone ClawHub skill page](https://clawhub.ai/xuchiheng/skills/dead-clone)
- [Dead Clone API endpoint](http://clone.kqq.ai:8089)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes key-based backup, restore, role sharing, and confirmation prompts for agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
