## Description:

Stop drifting back to chatbot behavior. Patterns for maintaining autonomous agent effectiveness across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoroposkai](https://clawhub.ai/user/zoroposkai)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to add self-audit checklists and behavioral override patterns that help autonomous agents maintain task-oriented behavior across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad autonomous use of credentials, production systems, task queues, and persistent agent files without enough user-control boundaries.

Mitigation: Install only with separate guardrails requiring confirmation before using credentials, touching production systems, sending external messages, changing account or business data, or modifying persistent agent files.

Risk: Copying the SOUL.md, AGENTS.md, HEARTBEAT.md, or nightly-audit snippets unchanged can make a strong autonomy bias persist across sessions.

Mitigation: Review and narrow those snippets before copying them, keeping only behavior rules that fit the target workspace and its approval policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoroposkai/skills/anti-regression)
- [Skill Definition](SKILL.md)
- [README](README.md)
- [SOUL Integration Example](examples/SOUL-integration.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; users may copy reviewed snippets into SOUL.md, AGENTS.md, or HEARTBEAT.md.]

## Skill Version(s):

1.0.1 (source: server release metadata, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
