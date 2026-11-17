## Description:

Claude Code Agent Teams orchestrates Claude Code's native agent teams feature for multi-lens reviews, competing-hypothesis debugging, full-stack features, architecture debates, and cross-domain investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew-a-gordon](https://clawhub.ai/user/matthew-a-gordon)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to coordinate multiple Claude Code agents on parallel work with clear roles, file boundaries, monitoring, and cleanup workflows. It is suited to reviews, debugging, full-stack implementation, architecture decisions, performance investigations, and data-parallel classification tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Force cleanup can terminate Claude PTY sessions beyond the intended team and may lose in-progress work.

Mitigation: Review scripts/team-cleanup.sh before use and prefer graceful cleanup. Avoid ./scripts/team-cleanup.sh --force --yes unless no other Claude PTY sessions are active and work loss is acceptable.

Risk: Spawned agents receive the repository and task context they are given and can materially increase token usage.

Mitigation: Limit shared context to what teammates need, define clear file and task boundaries, and right-size the team before spawning agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthew-a-gordon/skills/claude-code-teams)
- [Repository listed in artifact metadata](https://github.com/matthew-a-gordon/claude-code-teams)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with copy-paste prompts, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce team spawn prompts, review findings, debugging plans, ADR drafts, implementation coordination notes, and cleanup or monitoring commands.]

## Skill Version(s):

1.0.0 (source: package.json, SKILL.md metadata, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
