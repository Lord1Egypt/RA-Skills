## Description:

Loads anime character information from multiple sources and generates validated SOUL.generated.md persona files for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinchen4](https://clawhub.ai/user/colinchen4)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users, role-play communities, and developers use this skill to fetch anime character data, resolve ambiguous names, and generate reviewed SOUL persona files for agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Character and anime names may be sent to third-party anime and wiki services during lookup.

Mitigation: Install only when those external requests are acceptable for the intended use case, and avoid submitting sensitive or private names as queries.

Risk: Third-party character data can become persistent agent persona instructions in generated SOUL files.

Mitigation: Review SOUL.generated.md before using REPLACE or MERGE, with special attention to Background, Personality, Identity, and Boundaries text copied or summarized from remote sources.

Risk: REPLACE mode can overwrite an existing SOUL.md file.

Mitigation: Use KEEP or MERGE for review-first workflows and confirm backups before replacing an existing persona file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinchen4/skills/anime-character-loader)
- [AniList GraphQL API](https://graphql.anilist.co)
- [Jikan API](https://api.jikan.moe/v4)
- [README](artifact/README.md)
- [Baseline v2.4](artifact/docs/baseline-v2.4.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown persona files with CLI guidance and optional merge choices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates SOUL.generated.md and may merge or replace SOUL.md after user selection.]

## Skill Version(s):

2.4.2 (source: server release metadata, SKILL.md frontmatter, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
