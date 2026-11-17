## Description:

Play Apple Music songs on macOS using clawtunes with keyboard navigation to stream catalog tracks via the Music app and local library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skaravind](https://clawhub.ai/user/skaravind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to play songs, artists, albums, playlists, or moods in Apple Music on macOS when direct library playback is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates the macOS Music app through Accessibility and Automation permissions and can send catalog searches to Apple.

Mitigation: Review commands before running, grant permissions only in a trusted macOS session, and avoid sensitive search queries.

Risk: The bundled playlist_create.py script has an AppleScript injection risk when handling crafted playlist names.

Mitigation: Avoid using playlist_create.py with untrusted playlist names until its AppleScript handling is fixed or the script is removed.

Risk: Catalog playback depends on macOS UI focus and keyboard navigation, so playback may not switch to the requested song.

Mitigation: Check playback status after each attempt and report plainly when the requested track did not start.

## Reference(s):

- [Apple Music Play release page](https://clawhub.ai/skaravind/skills/apple-music-play)
- [Apple iTunes Search API endpoint](https://itunes.apple.com/search)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, the Music app, clawtunes, python3, osascript, open, and Accessibility/Automation permissions.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
