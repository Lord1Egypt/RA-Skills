## Description:

Scans the local desktop for installed music apps, launches them, and helps an agent recommend, search, or play music, with macOS AppleScript control for Spotify and Apple Music plus optional Spotify precise playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find installed music players, open a selected app, generate scene- or mood-based search suggestions, and initiate playback or control supported desktop players.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch local music apps and open music or search URLs, including user-provided file and URL targets.

Mitigation: Review the returned JSON target and result fields before treating an action as successful, and pass only files or URLs that the user explicitly requested.

Risk: macOS playback control depends on Accessibility and Automation permissions and can vary by client version, UI language, focus state, subscription status, and regional availability.

Mitigation: Grant only the required permissions to the host application, treat macOS UI playback as best effort, and fall back to search or open flows when control fails.

Risk: Optional Spotify precise playback uses an access token that could leak through command-line history or shared logs if supplied as an argument.

Mitigation: Prefer SPOTIFY_ACCESS_TOKEN over command-line token arguments, use a short-lived limited-scope token, and avoid sharing logs that contain token values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/desktop-music-launcher)
- [OpenClaw skill format documentation](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local app capability results, playback or search targets, best-effort flags, and permission requirements when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
