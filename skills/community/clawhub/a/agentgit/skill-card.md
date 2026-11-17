## Description:

Validates and merges multi-agent git work through a deterministic gate, requiring a real command to exit 0 before anything merges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tryboy869](https://clawhub.ai/user/tryboy869)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use AgentGit to gate sub-agent file changes with an objective validation command before accepting or merging them into a repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run and optionally link an unpinned external GitHub CLI with git and filesystem access.

Mitigation: Review the AgentGit repository before installation, prefer a pinned commit or signed release, avoid npm link unless the package is trusted, and use it only in repositories where that access is acceptable.

Risk: Validation and merge decisions are only as reliable as the configured project check.

Mitigation: Use a project-specific automated check such as tests, linting, schema validation, or compliance scripts, and surface the absence of an automated check instead of merging without validation.

## Reference(s):

- [AgentGit protocol documentation](https://github.com/Tryboy869/AgentGit/blob/main/docs/en/protocol.md)
- [AgentGit ClawHub skill page](https://clawhub.ai/tryboy869/skills/agentgit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and git binaries; validation behavior depends on the configured project check.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
