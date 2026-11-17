## Description:

Control Spotify playback: play, pause, resume, skip, previous, restart, search, queue, set volume, shuffle, repeat, and view now-playing status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ejatapibeda](https://clawhub.ai/user/ejatapibeda)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to control Spotify playback from a terminal or OpenClaw-compatible agent, including search, playback, queue, volume, shuffle, repeat, and now-playing status tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to provide raw Spotify browser session cookies and stores the session for reuse.

Mitigation: Use a dedicated or low-risk Spotify account where possible, avoid placing cookies in shell history or logs, and delete or rotate the stored session if exposure is suspected.

Risk: The skill installs an unpinned external SpotAPI dependency that receives Spotify session credentials.

Mitigation: Inspect the dependency before installation and prefer a pinned, reviewed commit or a safer OAuth-based authentication path.

## Reference(s):

- [ClawSpotify on ClawHub](https://clawhub.ai/ejatapibeda/skills/clawspotify)
- [SpotAPI dependency](https://github.com/ejatapibeda/SpotAPI)
- [Spotify Web Player](https://open.spotify.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [CLI command invocations and plain-text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require a saved Spotify session, an active Spotify account, and Spotify open on at least one device.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
