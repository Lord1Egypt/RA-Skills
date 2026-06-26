## Description: <br>
Bumblebee lets an agent control Spotify in two modes: speaking through exact lyric clips and curating context-aware music queues from time, mood, activity, and recent listening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r2d2-minero](https://clawhub.ai/user/r2d2-minero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search lyric indexes, play timestamped Spotify clips, manage playback, and queue music matched to the current context or requested mood. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control Spotify playback and read listening context through OAuth access. <br>
Mitigation: Install only if this level of Spotify account access is acceptable, review playback actions before use, and revoke the Spotify app authorization when no longer needed. <br>
Risk: The visible setup requests broader Spotify OAuth scopes than the core playback features require and stores long-lived credentials locally. <br>
Mitigation: Reduce OAuth scopes where possible, avoid playlist or library modification scopes unless needed, and keep .env and tokens.json private. <br>
Risk: Lyric indexes may contain copyrighted lyrics if users populate them from external sources. <br>
Mitigation: Build lyric indexes only from sources the user is authorized to use and do not distribute copyrighted lyric content with the skill. <br>


## Reference(s): <br>
- [Spotify Setup Guide](artifact/SETUP.md) <br>
- [Song Library Management](artifact/references/song-library.md) <br>
- [Building Your Lyric Index](artifact/scripts/build-lyric-index.md) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [Bumblebee on ClawHub](https://clawhub.ai/r2d2-minero/bumblebee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON summaries from local Node.js scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Spotify Premium, an active Spotify device, local Spotify OAuth credentials, and a user-managed lyric index.] <br>

## Skill Version(s): <br>
1.2.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
