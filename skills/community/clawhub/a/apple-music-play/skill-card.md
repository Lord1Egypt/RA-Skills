## Description: <br>
Play Apple Music songs on macOS using clawtunes, including streaming catalog tracks via a keyboard-navigation workaround after opening the song in Music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skaravind](https://clawhub.ai/user/skaravind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to play songs, artists, albums, playlists, or moods in Apple Music on macOS when direct library playback or normal AppleScript control is not enough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: macOS Accessibility and Automation permissions allow the scripts to send keyboard input to the Music app. <br>
Mitigation: Install only in trusted environments, review the scripts before use, grant permissions deliberately, and revoke them when no longer needed. <br>
Risk: Apple Music catalog searches send search terms to Apple. <br>
Mitigation: Avoid sensitive search queries and prefer direct library playback when search privacy matters. <br>
Risk: The playlist helper can create playlists and modify the user's Music library. <br>
Mitigation: Review or remove scripts/playlist_create.py if only playback is needed, and confirm intent before running playlist creation commands. <br>
Risk: Catalog playback relies on Music app UI focus and keyboard navigation, so it may not always play the requested track. <br>
Mitigation: Check the command's JSON status fields after playback attempts and state plainly when playback did not switch to the requested song. <br>


## Reference(s): <br>
- [Apple Music Play on ClawHub](https://clawhub.ai/skaravind/apple-music-play) <br>
- [Apple iTunes Search API endpoint](https://itunes.apple.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with Apple Music, clawtunes, python3, osascript, open, and Accessibility/Automation permissions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
