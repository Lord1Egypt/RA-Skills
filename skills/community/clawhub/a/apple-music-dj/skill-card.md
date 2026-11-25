## Description:

An Apple Music curator that analyzes listening history, builds personalized playlists, imports Spotify playlists, and provides music discovery and listening insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[and3rn3t](https://clawhub.ai/user/and3rn3t)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Apple Music listeners use the skill through an AI agent to understand their listening tastes, discover and organize music, import playlists, and review listening trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing possible account changes without the promised confirmation, behavior or activation phrases beyond the stated scope, and incomplete file inspection.

Mitigation: Consider avoiding installation until the account-change confirmation behavior and unattended playlist creation are reviewed and the partial scan coverage is resolved.

## Reference(s):

- [Feature guide](references/features.md)
- [Playlist strategies](references/playlist-strategies.md)
- [Authentication setup](references/auth-setup.md)
- [Spotify playlist import](references/spotify-import.md)
- [Security policy](SECURITY.md)
- [Apple Music API](https://api.music.apple.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Text and JSON reports, Markdown guidance, shell and Python commands, and optional playlist and profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May interact with the user's Apple Music account and local listening data; review account changes and scheduled jobs before use.]

## Skill Version(s):

3.5.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
