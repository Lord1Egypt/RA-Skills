## Description:

Captures learnings, errors, and corrections to enable continuous improvement for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suncrespo](https://clawhub.ai/user/suncrespo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, and feature requests as structured Markdown logs. They can review those entries later and promote broadly useful learnings into project memory after human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning entries or promoted memory can introduce incorrect or misleading guidance into future agent behavior.

Mitigation: Require a human-reviewed diff before promoting entries into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or copilot-instructions.md.

Risk: Optional hooks can run automatically and inspect prompt or tool-use context when enabled.

Mitigation: Keep hooks disabled unless explicitly needed, prefer project-scoped setup, and review hook scripts before enabling them.

Risk: Learning logs may capture sensitive context if raw output or transcripts are recorded.

Mitigation: Record short sanitized summaries and redact secrets, tokens, private keys, environment variables, and excessive source or configuration excerpts.

## Reference(s):

- [README](README.md)
- [Skill Definition](SKILL.md)
- [Hook Setup](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/suncrespo/skills/12123123123)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or append project-scoped .learnings Markdown files when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
