## Description: <br>
Helps an agent interact with a Crafty Controller REST API to manage Minecraft servers, files, backups, users, roles, schedules, logs, and console commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdstudios](https://clawhub.ai/user/zdstudios) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Minecraft server administrators use this skill to operate Crafty Controller instances through API-backed guidance, Python helper code, and command patterns for server administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control live Crafty Controller servers, including stop, kill, delete, restore, file write, permission, user, role, and configuration changes. <br>
Mitigation: Require manual confirmation before destructive or privilege-changing operations and limit the API key to only the permissions needed for the requested task. <br>
Risk: The skill requires a Crafty Controller API key and may expose broad server administration access if the token is shared or stored insecurely. <br>
Mitigation: Keep the token out of shared files and chats, rotate it if exposed, and avoid superuser tokens unless they are required. <br>
Risk: The helper examples disable TLS certificate verification for self-signed local Crafty installs. <br>
Mitigation: Enable certificate verification for non-local use and provide a trusted certificate path when connecting to remote Crafty Controller instances. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zdstudios/crafty-controller) <br>
- [Publisher profile](https://clawhub.ai/user/zdstudios) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided Crafty Controller host, port, and API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
