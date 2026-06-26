## Description: <br>
AI planning coach using the 4To1 Method to turn a 4-year vision into daily action, with support for Notion, Todoist, Google Calendar, or local Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingxuantang](https://clawhub.ai/user/qingxuantang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and personal productivity practitioners use this skill to set up and operate a 4To1 planning system, connect it to Notion, Todoist, Google Calendar, or local Markdown, and run daily, weekly, sprint, and quarterly reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Notion and Todoist API tokens in a plaintext config file. <br>
Mitigation: Prefer the local Markdown backend when possible, restrict file permissions on ~/.config/4to1/config, and rotate tokens if the file is exposed. <br>
Risk: The status script sources the local config file as shell code. <br>
Mitigation: Inspect ~/.config/4to1/config before running scripts/status.sh and keep only expected key-value assignments in that file. <br>
Risk: The skill may access personal planning data and external task or calendar services. <br>
Mitigation: Use tightly scoped integrations, review requested permissions, and limit connected workspaces to the planning data needed for the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingxuantang/4to1-planner) <br>
- [4To1 Planner website](https://4to1planner.com) <br>
- [4To1 Planner free starter kit](https://4to1planner.com/free-download.html) <br>
- [4To1 Planner templates](https://4to1planner.com/shop.html) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Todoist developer integrations](https://app.todoist.com/app/settings/integrations/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with conversational guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update planning records through configured Notion, Todoist, Google Calendar, or local Markdown backends.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
