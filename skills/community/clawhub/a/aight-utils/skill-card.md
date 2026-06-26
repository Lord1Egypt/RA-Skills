## Description: <br>
Native Aight app integration for creating reminders, tasks, triggers, and items. Use when user mentions deadlines, reminders, tasks, or tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vincenthhao](https://clawhub.ai/user/Vincenthhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn reminder, deadline, task, and tracking requests into structured Aight items with IDs, labels, schedules, and status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous reminder or task requests could create or update the wrong Aight item. <br>
Mitigation: Ask the user to confirm ambiguous requests before creating or changing reminders, tasks, deadlines, or tracked items. <br>
Risk: Natural language date parsing can schedule reminders for the wrong date, time, or timezone. <br>
Mitigation: Verify the interpreted date, time, and timezone with the user before saving scheduled reminders or deadlines. <br>
Risk: Failed item creation may place reminder or task details in local fallback files. <br>
Mitigation: Avoid adding highly sensitive details to Aight items and review local fallback files when creation fails. <br>


## Reference(s): <br>
- [Aight Utils on ClawHub](https://clawhub.ai/Vincenthhao/aight-utils) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Structured JSON snippets with concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated IDs, labels, ISO 8601 schedules, item types, and status updates for Aight reminders, tasks, triggers, and tracked items.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
