## Description:

Brain-inspired memory for AI agents that builds a semantic graph, applies spreading activation, lets unused memories decay, and reinforces useful memories with Q-value learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dario-github](https://clawhub.ai/user/dario-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to install and apply a semantic graph memory system for AI agents that need contextually relevant recall over long-running conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer clones or updates mutable GitHub code and installs it locally.

Mitigation: Review the repository contents before installation and install only from a trusted revision in a disposable directory or virtual environment.

Risk: The installer can remove the configured BIOMORPHIC_INSTALL_DIR if an update fails.

Mitigation: Use a dedicated installation directory, avoid pointing BIOMORPHIC_INSTALL_DIR at personal work, and do not run the installer with elevated privileges.

## Reference(s):

- [Biomorphic Memory homepage](https://github.com/dario-github/biomorphic-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+ and an embedding API.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
