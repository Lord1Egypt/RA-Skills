## Description:

Aider is a terminal AI pair-programming guide covering Git-integrated editing, multi-model setup, and code refactoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to set up and operate Aider for terminal-based AI pair programming, including selecting models, managing file context, running tests, and using Architect mode for refactoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading aider-chat directly in a shared Python environment can affect other tooling.

Mitigation: Install Aider in pipx or a virtual environment and consider pinning a known aider-chat version.

Risk: Aider can modify repository files and create commits based on AI-generated changes.

Mitigation: Work on a branch and review diffs before keeping or merging changes.

Risk: Remote AI providers may receive source code, secrets, logs, or test output shared during a session.

Mitigation: Do not send secrets, private code, or sensitive test output to remote providers unless that is acceptable for the project.

## Reference(s):

- [ClawHub Aider skill page](https://clawhub.ai/zhangifonly/skills/aider)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package installation commands, API key configuration examples, model selection flags, test commands, and repository-editing workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
