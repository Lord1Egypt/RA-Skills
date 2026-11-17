## Description:

Captures learnings, errors, and corrections so coding agents can record failures, user corrections, feature requests, outdated knowledge, and recurring improvements for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture actionable learnings, errors, and feature requests during coding-agent work, then review or promote recurring lessons into project memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files may capture broad conversational, command, or error context that includes secrets, personal data, or customer data.

Mitigation: Keep .learnings local by default, redact sensitive data before logging, and avoid storing raw command output.

Risk: Incorrect or misleading lessons could be promoted into future agent memory and affect later work.

Mitigation: Require human review before promoting learnings into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or copilot instructions.

Risk: Global hook setup or empty hook matchers can run reminders on every prompt.

Mitigation: Enable hooks intentionally, prefer project-scoped configuration, and review hook behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blockcloud/skills/cpppp)
- [OpenClaw Integration Guide](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update .learnings markdown files and project memory files after human review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
