## Description:

Stop making the same mistakes -- turn failures into patterns that prevent recurrence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent operators use Failure Memory to detect repeated test, API, error, deployment, and correction failures in a workspace, record observations with recurrence and confirmation counters, search and classify those observations, and identify patterns eligible for constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-local failure and correction memories may include noisy or inaccurate observations, especially from broad correction phrases.

Mitigation: Review `.learnings/` periodically and require human confirmation before using observations to generate or enforce constraints.

Risk: The skill writes memory files under `.learnings/` in the current workspace.

Mitigation: Install it only in workspaces where local failure and correction memory is appropriate for the trust boundary.

## Reference(s):

- [Failure Memory ClawHub Page](https://clawhub.ai/leegitw/skills/failure-memory)
- [Failure Memory Project Homepage](https://github.com/live-neon/skills/tree/main/agentic/failure-memory)
- [Live Neon Skills Repository](https://github.com/live-neon/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with command examples and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write workspace-local .learnings/ observation and learning files when used by an agent.]

## Skill Version(s):

1.5.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
