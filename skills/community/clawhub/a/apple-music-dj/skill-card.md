## Description:

Curates Apple Music playlists from listening history and offers personalized discoveries, taste insights, and optional account updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[and3rn3t](https://clawhub.ai/user/and3rn3t)

### License/Terms of Use:

MIT-0

## Use Case:

Apple Music subscribers use this skill to discover songs, build personalized playlists, compare listening tastes, and review their music history. A no-token demo lets prospective users explore its features first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to Apple Music developer and user tokens exposes music-account credentials.

Mitigation: Run token setup yourself and try the no-token demo before connecting your account.

Risk: Playlist, favorite, rating, and library changes can alter the user's music account.

Mitigation: Review previews and confirm the intended changes before enabling --create, --yes, or --apply.

Risk: Installed scheduled jobs can keep running and may make unattended changes.

Mitigation: Review the proposed cron jobs before installation, especially any job that creates playlists, and remove jobs when no longer needed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/and3rn3t/skills/apple-music-dj)
- [Project homepage](https://github.com/and3rn3t/apple-music-dj)
- [Apple Music API reference](artifact/references/api-reference.md)
- [Authentication setup](artifact/references/auth-setup.md)
- [Playlist strategies](artifact/references/playlist-strategies.md)
- [Spotify import](artifact/references/spotify-import.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, SVG]

**Output Format:** [Conversational text and playlist previews; optional SVG taste card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Playlist creation and account changes are opt-in; a no-token demo is available.]

## Skill Version(s):

3.4.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
