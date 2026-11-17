## Description:

Cli Toolkit Cn is a Chinese-language command-line helper for looking up common terminal commands, generating shell script templates, improving terminal workflows, and troubleshooting common command errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations engineers, and terminal users use this skill to get Chinese-language command examples, shell snippets, aliases, troubleshooting guidance, and basic script templates for common CLI tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied shell commands may include destructive file operations such as recursive deletion, bulk deletion, in-place edits, or cleanup of logs and temporary files.

Mitigation: Preview target files, take backups, and require explicit user confirmation before executing rm -rf, xargs rm, find -delete, sed -i, bulk rename, or similar destructive operations.

Risk: Troubleshooting guidance may suggest privileged commands or package installation with sudo.

Mitigation: Explain why elevated privileges are needed, prefer least-privilege alternatives, and require explicit confirmation before suggesting or running sudo commands.

Risk: Process management examples may include force-kill commands that can stop the wrong process or interrupt services.

Mitigation: Verify process identity and impact first, prefer graceful termination, and require confirmation before using kill -9, killall, or pkill patterns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/cli-toolkit-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language command examples and shell script templates; commands should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
