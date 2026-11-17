## Description:

Captures learnings, command failures, user corrections, feature requests, and better recurring approaches so agents can maintain structured improvement logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aceundefeated](https://clawhub.ai/user/aceundefeated)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record non-obvious learnings, errors, corrections, and requested capabilities in structured Markdown files, then promote durable guidance into project or workspace memory after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can capture sensitive session details or personal data.

Mitigation: Keep .learnings local by default and redact secrets, credentials, and personal data before logging.

Risk: Global or broad hooks can inject reminders across more agent sessions than intended.

Mitigation: Use hooks only after auditing the scripts and prefer scoped, opt-in hook configuration.

Risk: Promoting unreviewed learnings into agent instruction files can preserve incorrect or misleading guidance.

Mitigation: Require a human-reviewed diff before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, templates, and hook configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit reminder text through optional hooks and scaffold skill files when helper scripts are executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
