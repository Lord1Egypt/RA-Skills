## Description: <br>
Free Buddy Skills helps WorkBuddy discover opencode.ai free models and add them to the local WorkBuddy model configuration without requiring a user API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinke](https://clawhub.ai/user/pinke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WorkBuddy users and developers use this skill to fetch available opencode.ai free model IDs and configure them in their local WorkBuddy model list. It is intended for setup and update workflows where the user wants free model entries added or refreshed in ~/.workbuddy/models.json. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the local WorkBuddy model configuration file. <br>
Mitigation: Run it interactively, review proposed model additions, and keep a backup of ~/.workbuddy/models.json when the existing configuration matters. <br>
Risk: The skill depends on public opencode.ai model metadata being reachable and accurate at run time. <br>
Mitigation: Review the models it proposes before accepting changes and retry only after confirming network access if the model endpoint is unavailable. <br>
Risk: The release has no server-resolved import provenance for this version. <br>
Mitigation: For stricter supply-chain hygiene, review or pin the source before installing or distributing the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pinke/free-buddy-skills) <br>
- [opencode.ai models endpoint](https://opencode.ai/zen/v1/models) <br>
- [opencode.ai chat completions endpoint](https://opencode.ai/zen/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run an interactive Python script that fetches public model metadata and updates the local WorkBuddy models.json file after user confirmation.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
