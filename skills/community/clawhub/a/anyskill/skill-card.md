## Description:

AnySkill manages a GitHub-backed private skill cloud for agents, including skill discovery, on-demand loading, local download, upload, update, deletion, and pack installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyijianke](https://clawhub.ai/user/lanyijianke)

### License/Terms of Use:


## Use Case:

Developers and agent users use AnySkill to connect an agent to a private GitHub-backed skill repository, then find, load, download, publish, update, or remove agent skills across supported IDEs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a GitHub token to read from and write to a private skill repository.

Mitigation: Use a fine-grained token scoped to one repository, prefer read-only access unless upload or deletion features are needed, and avoid storing tokens in plaintext when the environment supports safer storage.

Risk: Mutable remote skill instructions can change what an agent loads or executes over time.

Mitigation: Install or load skills only from trusted sources and revisions, review remote changes before use, and do not install public packs unless the source is trusted.

Risk: Repository mutation features can modify persistent skill files and push or delete content.

Mitigation: Review diffs before git push or deletion, require explicit confirmation for destructive actions, and keep a recoverable repository history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyijianke/skills/anyskill)
- [AnySkill GitHub homepage](https://github.com/lanyijianke/AnySkill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce setup guidance, repository operations, file changes, and skill-management summaries based on the selected mode.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
