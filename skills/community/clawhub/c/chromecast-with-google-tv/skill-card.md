## Description: <br>
Cast YouTube videos, Tubi TV show episodes, and TV show episodes from other video streaming apps via ADB to Chromecast with Android TV (Chromecast 4K supported, Google TV Streamer support is unknown). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antgly](https://clawhub.ai/user/antgly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to pair with and control a Chromecast with Google TV from an agent workflow, including playback, pause, resume, status checks, and app-specific episode launch flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ADB Wireless Debugging, which grants control over the paired TV device. <br>
Mitigation: Install only from a trusted publisher, use explicit device and port values, and disable wireless debugging or revoke pairing when finished. <br>
Risk: URLs and show names are passed into device launch commands after limited validation. <br>
Mitigation: Pass only trusted Tubi URLs, YouTube inputs, app names, and show titles. <br>
Risk: Package override environment variables can redirect launch intents to alternate Android packages. <br>
Mitigation: Avoid package override environment variables unless they are intentionally needed and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antgly/chromecast-with-google-tv) <br>
- [Publisher profile](https://clawhub.ai/user/antgly) <br>
- [yt-api dependency module](https://github.com/nerveband/youtube-api-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill invokes local CLI tools and ADB commands against a paired Chromecast device.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and CHANGELOG, released 2026-02-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
