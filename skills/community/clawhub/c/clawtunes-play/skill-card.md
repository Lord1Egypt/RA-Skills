## Description:

Play Apple Music songs on macOS with clawtunes, including catalog tracks opened through Music when direct library playback is not enough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skaravind](https://clawhub.ai/user/skaravind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers on macOS use this skill to ask an agent to play songs, artists, albums, playlists, or moods in Apple Music, with fallback catalog search and UI navigation when library playback is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: macOS Automation or Accessibility permissions allow the skill to send UI input to Music, and playback can depend on the current Music UI state.

Mitigation: Grant permissions only on a trusted macOS account, review the actions before installation, and verify that playback changed to the requested track.

Risk: The package includes an undisclosed playlist/library modification script and the security evidence reports an AppleScript injection risk.

Mitigation: Do not invoke playlist or library modification scripts unless they have been reviewed and trusted; validate and escape playlist and track inputs before use.

Risk: Catalog playback sends search queries to the Apple iTunes Search API endpoint.

Mitigation: Avoid sensitive query text and confirm that network catalog searches are acceptable for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skaravind/skills/clawtunes-play)
- [Apple iTunes Search API endpoint](https://itunes.apple.com/search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on macOS Music UI state, local clawtunes availability, and Automation or Accessibility permissions.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
