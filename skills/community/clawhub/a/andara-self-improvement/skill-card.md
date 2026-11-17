## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atiati82](https://clawhub.ai/user/atiati82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and reusable best practices as persistent markdown records. The skill also guides when to promote high-value learnings into agent instruction or workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning records can capture sensitive conversation details, credentials, private URLs, raw transcripts, or environment data.

Mitigation: Keep `.learnings/` local or explicitly reviewed before committing, redact sensitive data, and avoid logging tokens, credentials, private URLs, raw transcripts, or full environment dumps.

Risk: Unreviewed promotion into future agent instruction files can preserve incorrect, misleading, or unwanted behavioral guidance.

Mitigation: Require a human diff review before adding promoted content to `CLAUDE.md`, `AGENTS.md`, Copilot instructions, `SOUL.md`, or `TOOLS.md`.

Risk: Always-on or global hooks can broaden the reminder behavior beyond the intended project scope.

Mitigation: Prefer project-scoped hooks with narrow matchers, avoid global hooks unless the scripts are trusted and audited, and periodically clean old learning records.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/atiati82/skills/andara-self-improvement)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, hook configuration examples, and markdown record templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs and propose promoted guidance for agent memory files when a user or agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
