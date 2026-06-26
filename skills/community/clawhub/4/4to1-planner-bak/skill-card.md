## Description: <br>
AI planning coach using the 4To1 Method to turn a four-year vision into daily action across Notion, Todoist, Google Calendar, or local Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to set up and run an AI-assisted planning system that links long-term vision, quarterly milestones, two-week sprints, daily tasks, and recurring reviews. The skill can connect to third-party planning services or maintain local Markdown planning files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Notion and Todoist tokens in a plaintext local config file. <br>
Mitigation: Restrict the config file to owner-only permissions, use dedicated low-privilege tokens or workspaces, and rotate tokens if they are exposed. <br>
Risk: The skill can read and write sensitive personal planning data in connected services or local files. <br>
Mitigation: Preview planned backend writes before allowing the agent to save them, and prefer the local Markdown backend or a dedicated planning workspace for sensitive data. <br>
Risk: Server security review reports package identity and setup inconsistencies. <br>
Mitigation: Review the publisher and package identity before installing, and confirm the release metadata matches the artifact being deployed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dorjenorbulim/4to1-planner-bak) <br>
- [4To1 Planner homepage](https://4to1planner.com) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Todoist developer integrations](https://app.todoist.com/app/settings/integrations/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with conversational guidance, inline shell commands, API examples, and planning templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update planning records in the selected backend or local Markdown files after user direction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
