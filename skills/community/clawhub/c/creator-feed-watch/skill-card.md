## Description: <br>
Tracks YouTube creators and analyzes video content, producing AI-powered summaries, key points, and optional new-upload notifications from YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glin23](https://clawhub.ai/user/glin23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to analyze YouTube videos, follow creator channels, and receive concise update cards when tracked channels publish new uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores followed YouTube creators and last-seen upload state in a local watchlist file. <br>
Mitigation: Set the watchlist path intentionally, especially on shared systems, and review local file access before deployment. <br>
Risk: Notification actions can send update messages through host-provided delivery adapters. <br>
Mitigation: Enable delivery only for expected targets and review configured destinations before running notification actions. <br>
Risk: The no-key YouTube path relies on public pages and feeds, which may be less reliable than API-backed resolution. <br>
Mitigation: Use a restricted YouTube API key when stronger creator resolution and upload checks are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glin23/creator-feed-watch) <br>
- [OpenClaw skill installation documentation](https://openclawdoc.com/docs/skills/installation) <br>
- [OpenClaw skill creation documentation](https://openclawdoc.com/docs/skills/creating-skills/) <br>
- [ClawHub publishing documentation](https://openclawdoc.com/docs/skills/clawhub/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON-compatible action results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized YouTube metadata, transcript availability, local watchlist state, notification payloads, and delivery results.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence, SKILL.md frontmatter, manifest.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
