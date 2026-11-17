## Description:

Captures learnings, errors, corrections, and reusable workflow improvements so coding agents can improve future sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinuscxj](https://clawhub.ai/user/dinuscxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture corrections, command failures, feature requests, and reusable best practices. The captured notes can later be reviewed and promoted into durable project or agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived notes may become persistent instructions that affect future agent behavior.

Mitigation: Review new learning entries and require human approval before promoting them into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Learning logs may capture secrets, sensitive prompts, or environment details.

Mitigation: Keep logs project-local by default and redact credentials, private prompts, and sensitive operational details before saving entries.

Risk: Global hooks can inject reminders across sessions where the publisher or scripts have not been reviewed.

Mitigation: Prefer project-local hook configuration and enable hooks only from a pinned or verified release that has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinuscxj/skills/analyzing-business-strategy-skill)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, hook snippets, and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead agents to create or update local learning logs, instruction files, hook configuration, or skill scaffolds when applied.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
