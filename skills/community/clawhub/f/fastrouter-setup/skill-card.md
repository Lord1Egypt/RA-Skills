## Description: <br>
Configures OpenClaw with FastRouter AI by fetching active text and vision-capable models from the FastRouter API and updating the local model provider configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vamsimnet](https://clawhub.ai/user/vamsimnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add or refresh a FastRouter provider configuration with the user's API key and the current FastRouter text or vision model list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies persistent OpenClaw configuration, including replacing the existing fastrouter provider section and adding default model entries. <br>
Mitigation: Review and back up ~/.openclaw/openclaw.json before applying changes, and confirm the provider replacement and default model additions are intended. <br>
Risk: The skill handles a user-provided FastRouter API key for local provider configuration. <br>
Mitigation: Provide only the intended FastRouter key, avoid sharing it in unrelated context, and inspect the generated configuration before saving. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vamsimnet/fastrouter-setup) <br>
- [FastRouter Models API](https://api.fastrouter.ai/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json and ask for approval before restarting the OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
