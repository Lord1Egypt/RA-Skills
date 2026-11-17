## Description:

Backup and restore your OpenClaw workspace to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickconstantinou](https://clawhub.ai/user/nickconstantinou)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use Clawsync to back up selected workspace identity files, skills, and scripts to a private GitHub repository and restore them when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restoring broad agent-control files, scripts, or skills could persist unwanted instructions.

Mitigation: Review each restored AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md, script, and skill before trusting or executing it.

Risk: Backup and Git operations could expose workspace content or affect local Git metadata when run in the wrong directory.

Mitigation: Use a private, dedicated backup repository and run the scripts only from the intended Clawsync backup directory.

Risk: Repository credentials could grant more access than this backup workflow needs.

Mitigation: Use a fine-grained GitHub token limited to the dedicated backup repository.

## Reference(s):

- [Clawsync on ClawHub](https://clawhub.ai/nickconstantinou/skills/clawsync)
- [nickconstantinou publisher profile](https://clawhub.ai/user/nickconstantinou)
- [ShellCheck](https://www.shellcheck.net/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BACKUP_REPO, OPENCLAW_WORKSPACE, and usually GITHUB_TOKEN or gh CLI authentication.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
