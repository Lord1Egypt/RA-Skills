## Description: <br>
Fitlog is a local Bash command-line productivity logger that records, searches, summarizes, and exports timestamped entries under ~/.local/share/fitlog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill as a local command-line logger for tasks, plans, progress notes, streaks, reminders, tags, reports, weekly reviews, searches, and exports. The release should be evaluated as a generic productivity logger rather than a workout-specific tracker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a fitness tracker, but the artifact implements a broader productivity logger. <br>
Mitigation: Evaluate and present the skill as a generic local productivity logger, not as a workout-specific tracker. <br>
Risk: User entries and exports may contain sensitive health, work, or personal details stored under ~/.local/share/fitlog. <br>
Mitigation: Avoid entering sensitive details unless local storage and export behavior are acceptable; manually remove ~/.local/share/fitlog when data should be cleared. <br>


## Reference(s): <br>
- [ClawHub Fitlog skill page](https://clawhub.ai/ckchzh/fitlog) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ckchzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only Bash workflow; stores logs and exports under ~/.local/share/fitlog.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact files report v2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
