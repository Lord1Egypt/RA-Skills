## Description:

View and manage Docker container processes and stats. Use when monitoring containers. Requires docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Dockerps to inspect Docker container lists, status, stats, processes, logs, and basic container state while monitoring Docker hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to the Docker daemon.

Mitigation: Install it only in environments where the agent is permitted to inspect and manage Docker resources.

Risk: The cleanup command can remove stopped containers and dangling images without warning.

Mitigation: Review the cleanup behavior before installation and require explicit confirmation or scoping before using it on shared or important Docker hosts.

## Reference(s):

- [Dockerps on ClawHub](https://clawhub.ai/bytesagain1/skills/dockerps)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker daemon access; cleanup can prune Docker resources outside the skill's own files.]

## Skill Version(s):

3.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
