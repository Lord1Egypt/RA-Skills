## Description:

OpenClaw/CatPaw agents use this skill to back up and restore workspace files, configuration, installed skills, selected system settings, and conversation context through a Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lipingjiang](https://clawhub.ai/user/lipingjiang)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw/CatPaw users use this skill to preserve agent configuration and context across changes, then restore workspace, configuration, or installed skill state when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic backups can upload sensitive OpenClaw workspace, configuration, session, memory, SSH, and system metadata to Git.

Mitigation: Use a private trusted repository, narrow the backup scope before installation, require a file manifest before each push, and exclude credentials, sessions, memory, SSH configuration, and system metadata by default.

Risk: Restore operations can copy unverified remote repository contents into trusted OpenClaw workspace, configuration, and skill locations.

Mitigation: Restore only from a verified commit after inspecting the diff, and prefer scoped restores for workspace, configuration, or skills instead of full restore.

Risk: Automatic and heartbeat-triggered backups may run without timely operator review.

Mitigation: Disable automatic and heartbeat backups unless explicitly needed, and require user approval before backup scripts push changes.

## Reference(s):

- [Setup guide](references/setup_guide.md)
- [ClawHub skill page](https://clawhub.ai/lipingjiang/skills/clone-lobster)
- [Meituan Code repository creation](https://dev.sankuai.com/code/create-repo)
- [Meituan Code SSH key settings](https://dev.sankuai.com/code/home)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command snippets and shell script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLONE_LOBSTER_REPO_URL and optional OPENCLAW_WORKSPACE or OPENCLAW_DIR environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
