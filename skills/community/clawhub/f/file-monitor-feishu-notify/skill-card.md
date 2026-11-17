## Description:

Monitors a configured local directory and sends Feishu group notifications when new files appear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyoujin-cd](https://clawhub.ai/user/huyoujin-cd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to watch a local folder and notify a Feishu group when new files are detected. It is suited for workflows where file arrivals need quick team visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs continuously and sends local file notifications to an external Feishu group.

Mitigation: Install it only for intentional monitoring workflows and configure a narrowly scoped watch directory.

Risk: The local config.json contains Feishu app credentials and chat routing details.

Mitigation: Protect config.json, avoid committing real secrets, and rotate credentials if they are exposed.

Risk: The pending notification file can influence outbound message content.

Mitigation: Restrict who can write to the pending notification file and the watched directory.

Risk: The artifact documentation includes unsafe operational patterns such as token-in-URL Git commands, npx @latest installation, and blanket python.exe termination.

Mitigation: Use safer credential handling, pin install commands where possible, and stop only the specific monitor process during uninstall or troubleshooting.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [ClawHub skill page](https://clawhub.ai/huyoujin-cd/skills/file-monitor-feishu-notify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local pending-notification markdown and Feishu text messages based on detected file events.]

## Skill Version(s):

1.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
