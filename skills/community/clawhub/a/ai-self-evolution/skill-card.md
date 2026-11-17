## Description:

Records agent learnings, errors, corrections, and feature requests in `.learnings/`, then prompts review and promotion of reusable lessons before and after major tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andylue](https://clawhub.ai/user/andylue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain project-local learning logs and reminders for recurring errors, user corrections, knowledge gaps, and reusable workflow improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived lessons may persist sensitive project details or secrets in `.learnings/` files.

Mitigation: Keep `.learnings/` project-local or gitignored unless intentionally shared, and redact secrets or sensitive project details before storing entries.

Risk: Logged lessons can be promoted into future agent instructions without strong review controls.

Mitigation: Review every write and promotion before committing or installing it globally.

Risk: Global hooks or full system-prompt installation can make the learning workflow broader than intended.

Mitigation: Prefer project-local use and avoid global hooks or full system-prompt installation unless explicitly needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/andylue/skills/ai-self-evolution)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Agent setup guide](references/agent-setup.md)
- [Hook setup guide](references/hooks-setup.md)
- [OpenClaw integration guide](references/openclaw-integration.md)
- [Skill extraction guide](references/skill-extraction.md)
- [Entry examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or update of `.learnings/` entries when enabled by the agent or hooks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
