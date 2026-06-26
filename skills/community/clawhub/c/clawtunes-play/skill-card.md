## Description: <br>
Play Apple Music songs on macOS using clawtunes, including streaming catalog tracks via a practical keyboard-navigation workaround after opening the song in Music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skaravind](https://clawhub.ai/user/skaravind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control Apple Music on macOS, play local library songs, search the Apple Music catalog, and attempt catalog playback through Music UI automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires macOS Accessibility or Automation permission and sends keyboard input to Music, so playback may affect the active Music UI state. <br>
Mitigation: Grant permissions only after review, run commands while Music is visible when possible, and verify the reported before and after track state. <br>
Risk: Catalog searches are sent to Apple through the iTunes Search API. <br>
Mitigation: Avoid using sensitive search terms and review network behavior before deployment in managed environments. <br>
Risk: The package includes an under-documented playlist script that can create playlists and change the user's Music library. <br>
Mitigation: Remove or avoid scripts/playlist_create.py when only playback is needed, and review commands before allowing library-modifying use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skaravind/clawtunes-play) <br>
- [Apple iTunes Search API endpoint](https://itunes.apple.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Apple Music, clawtunes, python3, osascript, open, and Accessibility or Automation permission for UI control.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
