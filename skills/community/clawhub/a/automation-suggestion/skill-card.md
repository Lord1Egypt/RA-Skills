## Description: <br>
Suggest automations only when they make sense, based on objective triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szpili](https://clawhub.ai/user/szpili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent suggest automation only after repeated or costly manual work, or clear user frustration, while applying cooldowns that reduce repeated suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses recent task history and message wording, including sentiment cues, to decide when to suggest automations. <br>
Mitigation: Install it only where that context use is acceptable, and prefer configurations that can disable sentiment-based triggers. <br>
Risk: Stored suggestion history may retain information about declined automations or repeated work patterns. <br>
Mitigation: Clear or limit stored suggestion history when the host agent provides memory controls. <br>


## Reference(s): <br>
- [Automation Suggestion skill page](https://clawhub.ai/szpili/automation-suggestion) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown suggestion text with optional configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Suggestion thresholds include minRepetitions, minWeeklyMinutes, and cooldownDaysAfterNo when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
