## Description:

Captures learnings, errors, and corrections so agents can log failures, user feedback, missing capabilities, and better recurring approaches for future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shendingyi](https://clawhub.ai/user/shendingyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture conversation-derived learnings, command errors, corrections, and feature requests in markdown files. They can review those entries and promote broadly useful patterns into persistent agent guidance after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived content may be persisted into future agent memory or instruction files without sufficient review.

Mitigation: Review every entry before saving or promotion, and do not promote entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions without human approval.

Risk: Learning logs can capture secrets, personal data, or sensitive project details.

Mitigation: Keep .learnings local and out of git unless deliberately approved, and redact secrets and personal data before writing entries.

Risk: Global hooks or empty matchers can add reminders to every prompt and make persistent logging feel automatic.

Mitigation: Use opt-in hook configuration, avoid global hooks or empty matchers unless desired, and prefer narrower activation when reminders should be limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shendingyi/skills/alex-self-improving-agent)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local markdown learning logs and persistent agent instruction files when the user applies the guidance or enables the optional hooks.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
