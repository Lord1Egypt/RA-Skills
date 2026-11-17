## Description:

Batch replaces remote URLs across Git repositories under a specified directory for repository migration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxfcn](https://clawhub.ai/user/zxfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill when migrating Git repositories between hosting servers and need agent-produced shell commands to update remotes in bulk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated commands can modify Git remote configuration across many repositories at once.

Mitigation: Use a narrowly scoped scan directory, review the commands before execution, and verify affected repositories with git remote -v afterward.

Risk: User-supplied paths and URLs can be unsafe when inserted directly into shell command templates.

Mitigation: Avoid untrusted path or URL inputs and prefer implementations that use git remote get-url and git remote set-url with a dry run or backup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxfcn/skills/batch-git-url-replace)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with PowerShell and Bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires scan directory, old URL, and new URL before generating commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
