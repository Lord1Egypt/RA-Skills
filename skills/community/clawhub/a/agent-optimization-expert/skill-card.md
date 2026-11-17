## Description:

Agent优化专家 diagnoses and helps repair agent execution issues such as cron failures, tool errors, workflow interruptions, and performance regressions across OpenClaw and Hermes Agent environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect agent and system state, classify cron, tool, workflow, and performance failures, propose fixes, and record learning patterns for OpenClaw or Hermes environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring self-repair and self-update workflows can modify local agent files or references.

Mitigation: Keep cron or heartbeat setup manual and review the exact proposed updates before applying them.

Risk: Maintenance actions can restart services, prune Docker resources, terminate sub-agents, or delete logs.

Mitigation: Require explicit approval for service restarts, Docker pruning, process termination, and file deletion.

Risk: Diagnostics inspect local agent and system state.

Mitigation: Run the skill only in workspaces where operational inspection is expected, and avoid recording secrets or sensitive data in logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/agent-optimization-expert)
- [Trigger Integration](artifact/TRIGGER-INTEGRATION.md)
- [Dual Environment Adaptation](artifact/references/dual-env-adaptation.md)
- [Error Taxonomy](artifact/references/error-taxonomy.md)
- [Fix Templates](artifact/references/fix-templates.md)
- [Self-Evolution Workflow](artifact/references/self-evolution.md)
- [Anthropic Engineering Patterns](artifact/references/anthropic-patterns.md)
- [OpenAI Agent Engineering Practices](artifact/references/openai-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic reports, fix proposals, validation checklists, and commands that require user approval before execution.]

## Skill Version(s):

1.4.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
