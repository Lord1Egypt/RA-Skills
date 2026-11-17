## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can preserve useful project knowledge and promote recurring patterns into durable guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log command failures, user corrections, knowledge gaps, feature requests, and repeatable best practices into markdown learning files. The skill also provides optional hook reminders and guidance for promoting broadly useful learnings into agent memory files or new skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files can preserve sensitive details or misleading conclusions across future sessions.

Mitigation: Keep learning logs project-scoped, avoid storing secrets or raw transcripts, and review entries before reuse.

Risk: Optional broad hooks can influence future agent behavior if enabled without review.

Mitigation: Review hook commands before enabling them, avoid global hook installation by default, and disable hooks that are not needed.

Risk: Promoting unreviewed learnings into shared agent memory can spread incorrect guidance.

Mitigation: Require human diff review before promoting content into CLAUDE.md, AGENTS.md, copilot instructions, SOUL.md, or TOOLS.md.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keyserkazi1/skills/auto-improvement)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning entries and optional setup instructions; users should review content before promotion into shared agent memory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
