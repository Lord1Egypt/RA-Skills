## Description:

Cast YouTube videos, Tubi TV show episodes, and TV show episodes from other video streaming apps via ADB to Chromecast with Android TV (Chromecast 4K supported, Google TV Streamer support is unknown)

This skill is ready for commercial/non-commercial use.

## Publisher:

[antgly](https://clawhub.ai/user/antgly)

### License/Terms of Use:


## Use Case:

Users with an ADB-paired Chromecast with Google TV use this skill to launch YouTube or Tubi content, open show episodes through Google TV global search, check device status, and send play or pause controls from a macOS or Linux host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a paired Google TV device through ADB.

Mitigation: Use it only on trusted hosts and networks, disable Wireless Debugging or remove unused pairings after use, and review commands before allowing device control.

Risk: The release installs and runs yt-api from an unpinned third-party Go module.

Mitigation: Pin or verify the yt-api dependency before relying on the installer in a managed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antgly/skills/chromecast-with-google-tv)
- [Publisher profile](https://clawhub.ai/user/antgly)
- [yt-api installer module](https://github.com/nerveband/youtube-api-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for an agent guiding or invoking local Chromecast control commands; successful use requires adb, scrcpy, uv, yt-api, and an authorized Google TV device.]

## Skill Version(s):

1.2.0 (source: release evidence and CHANGELOG, released 2026-02-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
