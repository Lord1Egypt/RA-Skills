## Description:

Production-grade AI coding agent for ZooClaw/OpenClaw following JT directives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyang1016](https://clawhub.ai/user/iyang1016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use Clawder to guide autonomous code changes with mandatory verification, root-cause bug fixing, edit integrity checks, sub-agent coordination, and persistent mistake logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous code-changing behavior can make unexpected edits or architectural refactors.

Mitigation: Run the skill in a clean branch or isolated worktree and review planned deletions or refactors before execution.

Risk: Persistent memory and gotchas logging can retain user, project, or feedback information beyond the current task.

Mitigation: Disable or audit memory and gotchas persistence when handling sensitive work.

Risk: Background-agent behavior can reduce direct user oversight of code changes.

Mitigation: Require review of sub-agent plans and outputs before merging or deploying changes.

Risk: Unpinned package-runner commands can execute registry-resolved code that changes over time.

Mitigation: Avoid unpinned npx troubleshooting commands unless the registry source and project configuration are trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iyang1016/skills/clawder-coding)
- [agent.md](artifact/agent.md)
- [SKILL.md](artifact/SKILL.md)
- [agent-card.json](artifact/agent-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to edit files, run verification commands, coordinate sub-agents, and maintain memory files.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
