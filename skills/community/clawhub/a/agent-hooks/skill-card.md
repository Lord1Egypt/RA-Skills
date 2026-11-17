## Description:

Agent Hooks provides drop-in Claude Code hook scripts for persistent execution, speculation checks, tool error escalation, and post-edit diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to install selected hooks that keep long-running tasks moving, discourage repeated failed tool calls, require evidence before speculative completion, and surface edit-time diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Stop hooks can force the agent to continue when the user expected a session to end.

Mitigation: Install only the needed hooks, avoid Ralph for short or low-risk work, set a low max iteration count, and keep ralph-cancel.sh available.

Risk: PreToolUse hooks can deny repeated tool calls and change normal agent execution flow.

Mitigation: Enable the tool-error hooks only where retry control is desired and review their thresholds before use.

Risk: Post-edit diagnostics can run local tools automatically, including an npx-based TypeScript check.

Mitigation: Review scripts before installation and replace or disable the npx TypeScript check unless it uses a pinned local dependency.

## Reference(s):

- [Agent Hooks on ClawHub](https://clawhub.ai/lanyasheng/skills/agent-hooks)
- [Claude Code Hooks documentation](https://code.claude.com/docs/en/hooks)
- [Oh My ClaudeCode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Ralph persistent execution pattern](references/01-ralph.md)
- [Tool error retry escalation pattern](references/03-tool-error.md)
- [Cancel signal TTL pattern](references/07-cancel-ttl.md)
- [Doubt gate pattern](references/13-doubt-gate.md)
- [Post-edit diagnostics pattern](references/15-post-edit-diagnostics.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON hook configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hook setup guidance and references to local bash scripts; installed hooks emit JSON decisions or additional context during Claude Code sessions.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact metadata; artifact SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
