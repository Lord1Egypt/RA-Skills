## Description:

Captures learnings, errors, corrections, and feature requests so agents can preserve useful context and improve future workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[china-mobile2008](https://clawhub.ai/user/china-mobile2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log non-obvious errors, user corrections, knowledge gaps, and reusable improvements into markdown learning files. It also guides promotion of stable lessons into project or workspace agent memory and supports optional hook-based reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs or memory files may capture secrets, user data, or sensitive project details.

Mitigation: Keep learnings project-local and redact secrets, credentials, and user data before saving or promoting entries.

Risk: Promoting entries into agent memory files can change future agent behavior across sessions.

Mitigation: Require human review before changing CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: Always-on or global hooks can make the reminder behavior broader than intended.

Mitigation: Avoid global hook setup, keep hooks opt-in per workspace, and use narrow hook matchers when hook reminders are enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/china-mobile2008/skills/12)
- [Self-improvement skill documentation](SKILL.md)
- [OpenClaw integration guide](references/openclaw-integration.md)
- [Hook setup guide](references/hooks-setup.md)
- [Entry examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of .learnings markdown logs and optional hook configuration; no API output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
