## Description:

Control internet radio playback with stream and station search, favorites, volume, pause/resume, stop, next, and current playback inspection using mpv or ffplay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[art-ps](https://clawhub.ai/user/art-ps)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control internet radio playback from an assistant or terminal, including stream playback, station lookup, favorites, volume, and playback status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playback controls can signal a persisted PID without verifying it still belongs to the player process.

Mitigation: Validate the stored PID belongs to the expected player before sending signals, and review before installing where important long-lived processes run in the same user account.

Risk: Station search contacts the external Radio Browser API.

Mitigation: Document the outbound station-search request and use direct stream URLs or built-in stations where external lookup is not approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/art-ps/skills/agent-radio)
- [Radio Browser station search API](https://de1.api.radio-browser.info/json/stations/byname/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text command responses and shell command effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local preferences and playback state in JSON files.]

## Skill Version(s):

0.1.1 (source: server release metadata; source SKILL.md frontmatter lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
