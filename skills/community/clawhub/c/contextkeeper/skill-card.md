## Description:

ContextKeeper helps agents save local project checkpoints and view recent project status using manual bash scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopinathnelluri](https://clawhub.ai/user/gopinathnelluri)

### License/Terms of Use:


## Use Case:

Developers and agent users use ContextKeeper to preserve local work context across sessions by creating checkpoint summaries and viewing recent project state, git branch, modified files, and checkpoint history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint messages and project metadata are persisted locally under ~/.memory/contextkeeper.

Mitigation: Avoid putting secrets or sensitive project details in checkpoint messages, and review generated checkpoint files before using the skill on sensitive projects.

Risk: The security evidence reports unsafe parsing and path-handling concerns around timestamp parsing, project ID validation, file permissions, and symlink/file creation behavior.

Mitigation: Review and fix those behaviors before running the scripts on sensitive projects or shared systems.

Risk: The scripts collect local git branch, recent commit, and modified-file metadata from the current repository.

Mitigation: Run the scripts only in intended repositories and inspect persisted state if repository metadata should not be retained.

## Reference(s):

- [ContextKeeper Implementation Guide](references/implementation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, terminal text, and local JSON checkpoint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When scripts are run, they write checkpoint state under ~/.memory/contextkeeper and may persist checkpoint messages and git metadata.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
