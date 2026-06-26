## Description: <br>
Tracks Diablo IV world boss spawn countdowns from the Caimogu map and prompts for a reminder when a boss is upcoming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crazzies](https://clawhub.ai/user/Crazzies) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Diablo IV players can ask an agent for the current world boss, spawn status, and countdown. When the boss is not active, the skill guides the agent to ask whether the user wants a reminder before the expected spawn time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes a public web request to retrieve current Diablo IV world boss timing data. <br>
Mitigation: Install only if that request is acceptable in the user's environment and treat the external timing data as informational. <br>
Risk: Reminder behavior may create scheduled notifications when the user asks for them. <br>
Mitigation: Review any reminder entries after creation so the user knows when they run and how to remove them. <br>


## Reference(s): <br>
- [Caimogu Diablo IV map](https://map.caimogu.cc/d4.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown-like plain text with boss name, status, countdown, source link, and reminder prompt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public map data at query time; reminder setup is suggested only when countdown or waiting status is reported.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
