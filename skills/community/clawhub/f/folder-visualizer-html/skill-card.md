## Description:

A security-hardened visual directory tree generator that creates a collapsible HTML visualization of local folders with XSS protection and shell-injection defenses, designed for mobile viewing via Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdsds222](https://clawhub.ai/user/sdsds222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to inspect local directories by generating a self-contained collapsible HTML report and, when configured, delivering it via Telegram for mobile viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send folder names, paths, file sizes, and modification dates to Telegram while its privacy note says no third-party upload occurs.

Mitigation: Use it only on directories whose metadata can be shared through Telegram; make Telegram export opt-in and correct the privacy statement before release.

Risk: Directory metadata may expose sensitive project structure, confidential file names, or private local paths.

Mitigation: Review the target directory before execution and avoid sensitive home directories, secret stores, and confidential repositories.

Risk: Recursive traversal may cover symlinks or very large directory trees without explicit limits.

Mitigation: Skip or constrain symlinks and add traversal depth or item limits before using the skill on broad paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdsds222/skills/folder-visualizer-html)
- [Publisher profile](https://clawhub.ai/user/sdsds222)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a generated self-contained HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a Telegram bot token for Telegram delivery; generated local reports should be deleted after delivery.]

## Skill Version(s):

1.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
