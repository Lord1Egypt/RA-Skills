## Description: <br>
Aqara Agent lets an assistant use the Aqara Open API to manage smart-home spaces, query and control devices, create ambience scenes, manage scenes and automations, and report energy statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqara](https://clawhub.ai/user/aqara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home operators use this skill to connect an agent to Aqara Home, choose a home, inspect device and room state, send supported device commands, create ambience scenes, manage automations, and review energy usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide an Aqara API credential that can control a smart home. <br>
Mitigation: Install only from a trusted publisher, verify the login and API URLs, avoid sharing the credential in exposed workspaces or chat history, and rotate or revoke the key if exposure is possible. <br>
Risk: The skill stores the Aqara credential locally in assets/user_account.json. <br>
Mitigation: Treat assets/user_account.json as a secret, keep it out of shared logs and source control, and remove or rotate the credential when the workspace is no longer trusted. <br>
Risk: Supported workflows can change real devices, scenes, firmware, and automations. <br>
Mitigation: Review command targets before execution and avoid broad or security-sensitive smart-home commands unless the intended home, room, device, scene, or automation is clear. <br>


## Reference(s): <br>
- [Aqara Agent on ClawHub](https://clawhub.ai/aqara/aqara-agent) <br>
- [Aqara account management](references/aqara-account-manage.md) <br>
- [Home and space management](references/home-space-manage.md) <br>
- [Device inquiry](references/devices-inquiry.md) <br>
- [Device control](references/devices-control.md) <br>
- [Ambience and lighting effects](references/ambience.md) <br>
- [Scene management](references/scene-manage.md) <br>
- [Automation management](references/automation-manage.md) <br>
- [Automation creation](references/automation-create.md) <br>
- [Energy statistics](references/energy-statistic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise natural-language summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue Aqara Open API calls through bundled Python scripts after the user provides required credentials and selects a home.] <br>

## Skill Version(s): <br>
0.1.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
