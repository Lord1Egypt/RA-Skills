## Description:

Delegates coding and analysis tasks to Claude Code CLI, captures the result, and reports it back in chat with support for continued sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmanel](https://clawhub.ai/user/0xmanel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to delegate coding, file analysis, test-writing, and follow-up implementation tasks to Claude Code CLI from an agent chat. The skill is useful when a task benefits from Claude Code's project context, shell access, and persistent per-directory sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated Claude Code runs with permission checks bypassed and weak workspace controls.

Mitigation: Use only in a sandboxed project directory, avoid sensitive workspaces, and remove or disable permission-bypass mode before trusted use.

Risk: Delegation or session continuation can perform actions using prior project context.

Mitigation: Require explicit confirmation before delegation or continuation and review captured output before relying on changes or recommendations.

Risk: Installer behavior can change if the install source is not pinned.

Mitigation: Pin the installer version when installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xmanel/skills/ask-claude-skill)
- [OpenClaw](https://openclaw.dev)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown chat response with captured CLI output and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stderr, exit codes, edited file names, and summarized long outputs.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact package.json and README changelog list 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
