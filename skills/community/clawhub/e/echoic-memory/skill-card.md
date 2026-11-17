## Description:

Echoic Memory helps users create local memorial AI Skills from chat history, photos, videos, voice memos, social media, and written memories to preserve a departed person's personality, expressions, and memories.

This skill is for research and development only.

## Publisher:

[quqicolour](https://clawhub.ai/user/quqicolour)

### License/Terms of Use:

MIT-0

## Use Case:

External users run the skill in Claude Code or OpenClaw to build a private memorial persona skill for someone who has died, left, or become unreachable. The workflow imports personal source material, generates memory and persona files, and supports later corrections or added memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes very private chat archives, photos, videos, voice messages, and written memories.

Mitigation: Use only material you are authorized to process, redact third-party and location-sensitive details, and keep the generated echoes directory out of cloud sync.

Risk: Generated memorial skills persist AI impersonation instructions for real people.

Mitigation: Clearly treat each generated memorial as an AI simulation, keep respectful boundaries, and seek professional support when grief becomes overwhelming.

Risk: Local delete, rollback, and media-analysis paths were flagged for review.

Mitigation: Avoid those paths until slug validation, safe deletion behavior, and eval removal are fixed; keep backups before changing or deleting generated skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quqicolour/skills/echoic-memory)
- [README](artifact/README.md)
- [Architecture](artifact/docs/ARCHITECTURE.md)
- [Product requirements](artifact/docs/PRD.md)
- [Cross-platform guide](artifact/docs/CROSS_PLATFORM.md)
- [WeChatMsg](https://github.com/LC044/WeChatMsg)
- [PyWxDump](https://github.com/xaoyaoo/PyWxDump)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and generated local Markdown, JSON, and skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates files under echoes/{slug}/, including memory.md, persona.md, meta.json, SKILL.md, version backups, and optional source-material folders.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
