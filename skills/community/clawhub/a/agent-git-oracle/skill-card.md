## Description:

Advanced repository analysis and refactoring guide. Identifies technical debt and architectural anti-patterns using AI reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to analyze local git repositories for technical debt, architectural anti-patterns, and refactoring opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented usage runs an unpinned external CLI package.

Mitigation: Use a pinned, reviewed OpenClaw CLI version from a trusted registry or lockfile before running the skill.

Risk: Repository contents may be processed by paid compute during analysis.

Mitigation: Confirm how repository contents are handled before using the skill on private projects or code that may contain secrets.

## Reference(s):

- [Agent Git Oracle on ClawHub](https://clawhub.ai/tmstudio667-commits/skills/agent-git-oracle)
- [tmstudio667-commits ClawHub profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with repository analysis, refactoring guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May analyze repository contents through an external OpenClaw CLI invocation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
