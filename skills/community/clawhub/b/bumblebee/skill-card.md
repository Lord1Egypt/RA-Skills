## Description:

Bumblebee lets an OpenClaw agent control Spotify to communicate through exact lyric clips and curate context-aware music queues based on mood, activity, time, and recent listening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r2d2-minero](https://clawhub.ai/user/r2d2-minero)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use Bumblebee to make an agent play Spotify lyric clips as short messages or build a music queue for a requested vibe. It requires Spotify Premium, an active Spotify device, and locally stored Spotify OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Spotify OAuth scopes may grant more account access than basic playback needs.

Mitigation: Review requested scopes before authorization and grant playlist or library permissions only when those features are needed.

Risk: Local Spotify client secrets and refresh tokens can affect account playback if exposed.

Mitigation: Store projects/spotify/.env and tokens.json with owner-only permissions, keep them out of shared artifacts and version control, and rotate credentials if exposed.

Risk: The helper scripts can change the active Spotify device, queue, volume, and playback state.

Mitigation: Check the target device before playback and confirm user intent before queue, volume, or playback changes.

## Reference(s):

- [Bumblebee ClawHub Release](https://clawhub.ai/r2d2-minero/skills/bumblebee)
- [Song Library Management](references/song-library.md)
- [Building Your Lyric Index](scripts/build-lyric-index.md)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, terminal commands, and JSON summaries from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Spotify credentials and an active Spotify device; lyric indexes must be user-provided or built from permitted sources.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
