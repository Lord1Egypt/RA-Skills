## Description:

Captures learnings, errors, and corrections so coding agents can preserve reusable knowledge and improve future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and reusable practices in markdown learning logs. They can optionally promote reviewed patterns into persistent agent instruction files or extracted skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can retain sensitive details if secrets, raw transcripts, or private operational context are copied into `.learnings/`.

Mitigation: Use project-local learning files, keep secrets and raw transcripts out of logs, and review entries before sharing or committing them.

Risk: Promoting learnings into agent instruction files can make behavior changes durable across future sessions.

Mitigation: Require a reviewed diff before updating AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Always-on or broad hook matchers can inject reminders more widely than intended.

Mitigation: Prefer project-level setup, avoid global hooks unless explicitly needed, and replace empty matchers with narrow trigger patterns where practical.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fangwei-frank/skills/frank-self-improving-agent)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown learning entries, setup snippets, hook reminder text, shell commands, and skill scaffold files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional hooks emit reminder text; the extraction helper can create a new skill scaffold under a relative local skills directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
