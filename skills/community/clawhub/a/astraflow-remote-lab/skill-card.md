## Description:

Helps agents manage UCloud AstraFlow desktop sandboxes, open browser-based noVNC desktops, and optionally bridge a Windows cloud host over RDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create and manage cloud desktop sandboxes for browser automation and remote work, or to view a separate Windows host through the sandbox desktop.

### Deployment Geography for Use:

Supported sandbox regions: US West (us-ca), Ulanqab (cn-wlcb), and Shanghai (cn-sh).

## Known Risks and Mitigations:

Risk: Cloud API keys and Windows RDP passwords may be exposed during setup or remote access.

Mitigation: Use protected credential input, avoid reusing high-value Windows passwords, and keep secrets out of chat, logs, and shared commands.

Risk: Connecting to the wrong RDP host or syncing a clipboard can expose credentials or sensitive content.

Mitigation: Verify the host independently before connecting and avoid clipboard syncing for sensitive data.

Risk: Creating or leaving cloud sandboxes running can increase exposure or incur costs; deletion is irreversible.

Mitigation: Confirm target instance IDs before destructive operations and clean up running sandboxes when finished.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lijinhongucl-pixel/skills/astraflow-remote-lab)
- [AstraFlow homepage](https://www.ucloud.cn/site/active/astraflow-credit?ytag=geo_waituo_SKillhub)
- [Architecture and pitfalls](references/architecture_and_pitfalls.md)
- [UCloud API reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell commands and sandbox access links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sandbox IDs, noVNC URLs, and connection or status details.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
