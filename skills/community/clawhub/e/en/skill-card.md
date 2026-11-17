## Description:

Captures learnings, errors, and corrections so agents can maintain local improvement logs and promote recurring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weina0925](https://clawhub.ai/user/weina0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record corrections, command failures, feature requests, and reusable workflow lessons in local markdown logs before promoting proven guidance to agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent changes to future agent guidance files.

Mitigation: Review any proposed changes to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions before they are written.

Risk: All-prompt hook examples can make reminders active across broad scopes.

Mitigation: Prefer project-local .learnings and project-level hooks; avoid global hook configuration unless all-project activation is intended.

Risk: Learning logs or cross-session sharing could capture sensitive transcripts, secrets, tokens, or command output.

Mitigation: Store short redacted summaries, keep logs local by default, and share across sessions only in trusted environments with explicit user intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weina0925/skills/en)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation and maintenance of local learning logs; optional hooks emit reminders when explicitly configured.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
