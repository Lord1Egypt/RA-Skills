## Description:

Captures learnings, errors, and corrections so agents can log recurring discoveries, command failures, user corrections, and missing capabilities for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture project learnings, errors, and feature requests in markdown logs, then promote durable patterns into agent memory or instruction files after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and memory promotion can capture sensitive or overly broad project context.

Mitigation: Keep logs project-local, avoid secrets and raw conversation text, and review entries before promotion.

Risk: Global or broad hook activation can inject reminders across unrelated workspaces and increase unintended persistence.

Mitigation: Use opt-in project-level hooks with restrictive matchers and avoid user-level global hooks unless explicitly needed.

Risk: Promoting learnings into agent instruction files can change future agent behavior across sessions.

Mitigation: Require human review before adding content to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: The extraction helper can create new skill files from logged learnings.

Mitigation: Run the helper in dry-run mode first and inspect the generated scaffold before writing files.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/yequanzheng/skills/cook-every-thing-3)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and log-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local learning logs and generated skill scaffolds when the user or agent runs the provided helper scripts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
