## Description: <br>
Guides OpenClaw users through generating Feishu bot configuration snippets and binding them to OpenClaw agents in openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill when setting up or updating Feishu bot integrations, including account-level and group-level agent bindings. It provides configuration snippets and manual setup guidance without directly modifying local configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper displays the provided Feishu App Secret in clear text when printing configuration snippets. <br>
Mitigation: Use it only in a private terminal, avoid sharing secrets in chats, screenshots, logs, or source control, and rotate the App Secret if it is exposed. <br>
Risk: Generated configuration snippets may need to be placed into openclaw.json manually. <br>
Mitigation: Review the generated openclaw.json changes before applying them and restart OpenClaw Gateway only after confirming the configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joe12801/feishu-agent-config-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Terminal text with Markdown code blocks containing JSON snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-provided Feishu identifiers and may display the App Secret in generated configuration snippets.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
