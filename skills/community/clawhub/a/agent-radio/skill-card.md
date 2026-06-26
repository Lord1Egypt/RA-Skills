## Description: <br>
Control internet radio playback with stream and station search, favorites, volume, pause/resume, stop, next, and current playback inspection using mpv or ffplay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[art-ps](https://clawhub.ai/user/art-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agent operators use this skill to play internet radio streams, search stations, manage favorites, and control local playback from an assistant or terminal session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playback can continue in the background through mpv or ffplay. <br>
Mitigation: Use the stop command when finished and check current playback status when needed. <br>
Risk: Station search and playback connect to external internet radio services. <br>
Mitigation: Use trusted stream URLs and avoid sensitive search terms when using station search. <br>
Risk: Favorites, volume, last station, and playback state are saved in local preference files. <br>
Mitigation: Review the configured preference path and protect or delete saved preferences according to local privacy requirements. <br>


## Reference(s): <br>
- [Agent Radio on ClawHub](https://clawhub.ai/art-ps/agent-radio) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text command output and persisted JSON preferences] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch background mpv or ffplay playback and update local preferences.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
