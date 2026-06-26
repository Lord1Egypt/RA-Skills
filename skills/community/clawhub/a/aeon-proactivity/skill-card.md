## Description: <br>
Aeon Proactivity helps an agent learn from user feedback, keep local notes, remember preferences and reminders, and suggest safer or more efficient next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent a local proactivity framework for remembering corrections, preferences, time-bound reminders, successful approaches, and configuration changes. It is intended for agents that should adapt across sessions while keeping notes in the user's local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores corrections, preferences, reminders, and session notes locally, which could capture sensitive details if users provide them. <br>
Mitigation: Avoid giving the agent secrets or sensitive personal details, and periodically inspect or delete the files under ~/.openaeon/workspace/. <br>
Risk: Stored preferences, reminders, or prior-session summaries can become stale or misleading over time. <br>
Mitigation: Review local memory files periodically and remove outdated, conflicting, or unwanted entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gu2003li/aeon-proactivity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, text guidance, and suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory files under ~/.openaeon/workspace/ when local storage permissions are available.] <br>

## Skill Version(s): <br>
2.7.0 (source: server evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
