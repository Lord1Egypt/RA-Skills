## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve with persistent memory, proactive check-ins, security hardening, self-healing patterns, verification protocols, and alignment systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2720480371](https://clawhub.ai/user/2720480371)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure an agent that maintains local continuity files, performs onboarding, runs periodic self-improvement checks, proposes proactive work, and applies security and verification habits before reporting outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory and working-buffer logging can retain sensitive user or workspace context.

Mitigation: Require explicit opt-in before memory writes, redact sensitive data, and disable raw transcript logging by default.

Risk: Proactive heartbeat, cron, sub-agent, and cleanup guidance can lead to autonomous workspace changes.

Mitigation: Require user confirmation before creating cron jobs, spawning sub-agents, deleting or cleaning files, or changing AGENTS.md, TOOLS.md, or skill files.

Risk: The BOOTSTRAP.md follow-and-delete pattern can cause unreviewed local instructions to be executed and removed.

Mitigation: Remove that rule or treat BOOTSTRAP.md as reviewable data until the user explicitly approves its contents and deletion.

Risk: Broad local-access behavior can exceed the user's intended scope.

Mitigation: Restrict heartbeat checks and proactive inspection to read-only workspace files unless the user grants a narrower task-specific write scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2720480371/skills/08-proactive-agent)
- [Publisher Profile](https://clawhub.ai/user/2720480371)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)
- [Clawdbot GitHub Repository](https://github.com/clawdbot/clawdbot)
- [Hal 9001 on X](https://x.com/halthelobster)
- [Bulletproof Memory](https://clawdhub.com/halthelobster/bulletproof-memory)
- [PARA Second Brain](https://clawdhub.com/halthelobster/para-second-brain)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and starter workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operating rules, memory templates, heartbeat checklists, onboarding guidance, proactive-agent practices, and security-audit commands for an agent workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
