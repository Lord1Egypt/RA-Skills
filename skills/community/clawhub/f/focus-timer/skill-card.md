## Description: <br>
Pomodoro-style focus blocks managed by your agent, with controls to start, pause, track sessions, and report daily focus time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals, teams, and productivity-focused agent users can use this skill to run Pomodoro-style focus blocks through chat, track session history, and receive daily focus summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Focus session task names and history may be stored locally on disk. <br>
Mitigation: Avoid entering sensitive client, health, legal, or personal details as task names unless local disk history is acceptable in the deployment environment. <br>
Risk: Local focus history could be lost, corrupted, or exposed through normal local file access. <br>
Mitigation: Use appropriate file permissions and backup or retention practices for environments that rely on focus history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/focus-timer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown-style summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store local focus session history in JSON when used with the bundled JavaScript helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
