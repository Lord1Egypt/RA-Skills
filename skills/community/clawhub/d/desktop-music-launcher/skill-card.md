## Description: <br>
Scans locally installed music apps, opens them, and helps an agent recommend, search, or play music, with macOS AppleScript controls for Spotify and Apple Music plus an optional Spotify precise-play path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to inspect desktop music-player availability, open players, generate searchable music recommendations, and control playback where local permissions and player capabilities allow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open and control local desktop music apps, including macOS desktop automation. <br>
Mitigation: Install only when that local control is desired, and grant Accessibility or Automation only to trusted host applications. <br>
Risk: Optional Spotify access tokens may be exposed through shell history or logs if handled carelessly. <br>
Mitigation: Use short-lived, minimally scoped tokens and avoid placing them in shared logs or persistent command history. <br>
Risk: Search or playback may fail or select a different result because local player state, permissions, account status, region, subscriptions, and client UI vary. <br>
Mitigation: Treat playback as best effort and rely on returned command results instead of asserting success without verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/desktop-music-launcher) <br>
- [OpenClaw skill format documentation](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should reflect script-returned results and should not claim playback succeeded unless the local command output confirms it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
