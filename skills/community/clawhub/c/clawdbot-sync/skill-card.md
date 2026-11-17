## Description:

Synchronizes memory, preferences, and skills between Clawdbot instances using SSH and rsync over Tailscale or direct network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:

MIT

## Use Case:

Developers and ClawHub users use this skill to configure trusted peers and synchronize agent memory, profile files, and selected skill data across their own Clawdbot instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill syncs sensitive agent memory and profile data between machines.

Mitigation: Use it only with trusted peers, run /sync diff before transfer, review memory changes before pulling or bidirectional sync, and keep backups.

Risk: Remote SSH writes can affect another workspace if peer access or host trust is misconfigured.

Mitigation: Pin or verify SSH host keys, restrict peers to a dedicated low-privilege account, and constrain sync to an intended workspace path.

Risk: The setup material includes a Tailscale install one-liner.

Mitigation: Replace it with verified package-manager installation instructions before use.

## Reference(s):

- [Clawdbot Sync release page](https://clawhub.ai/udiedrichsen/skills/clawdbot-sync)
- [Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires rsync, ssh, and jq; remote sync depends on configured SSH peers.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
