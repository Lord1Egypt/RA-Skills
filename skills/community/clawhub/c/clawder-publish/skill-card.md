## Description:

A production-grade AI coding agent that enforces JT directives by verifying code, running parallel sub-agents, logging mistakes, and ensuring edit integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyang1016](https://clawhub.ai/user/iyang1016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this coding agent to work on ZooClaw/OpenClaw projects with stricter verification, edit integrity, sub-agent coordination, and memory-based mistake tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous code-editing and command-running authority could change files or execute commands beyond the user's intent.

Mitigation: Install and run the skill only in trusted repositories or an isolated environment, and review commands and file changes before accepting them.

Risk: Persistent memory and gotchas logging may retain sensitive transcript or project details.

Mitigation: Disable or review persistent memory and gotchas logging, and avoid saving private or secret information in memory files.

Risk: Bypass or yolo-style execution modes reduce user control over destructive or high-impact actions.

Mitigation: Use approval-based modes for normal work and avoid bypass or yolo modes unless broad file and command access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iyang1016/skills/clawder-publish)
- [Clawder agent definition](artifact/clawder/agent.md)
- [Clawder agent card metadata](artifact/clawder/agent-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform code edits, run verification commands, and write memory files when granted agent privileges.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, agent-pack.yaml, agent-card.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
