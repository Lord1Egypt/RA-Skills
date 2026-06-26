## Description: <br>
BetterPrompt helps agents discover, install, and run reusable AI prompt skills from the BetterPrompt registry through the betterprompt or bp CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeqle](https://clawhub.ai/user/mikeqle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search BetterPrompt skills, inspect required inputs and model choices, generate text, image, or video outputs, and manage installed prompt skills across supported agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation, login, uploads, and skill management call an external BetterPrompt CLI service. <br>
Mitigation: Confirm intent and data sensitivity before logging in, sending prompts or local files, generating outputs, installing skills, or updating skills. <br>
Risk: Global scope or wildcard uninstall can affect skills across agents. <br>
Mitigation: Confirm the target agent and scope before install, uninstall, update, or removal actions, especially when using global scope or wildcard uninstall. <br>


## Reference(s): <br>
- [BetterPrompt Skill Homepage](https://betterprompt.me/skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/mikeqle/betterprompt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Images, Video] <br>
**Output Format:** [Markdown with inline shell commands; BetterPrompt CLI commands may return JSON, text, image, or video outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured JSON flags for machine-readable CLI responses when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
