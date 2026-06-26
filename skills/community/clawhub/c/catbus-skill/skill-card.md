## Description: <br>
CatBus helps an agent install and bind to the CatBus network, then route requests to remote models and skills for stronger model access, search, paper lookup, image generation, text-to-speech, and video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1997434](https://clawhub.ai/user/yang1997434) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect a local agent to CatBus, bind it to an account, and forward selected tasks to CatBus-hosted models or remote skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to run a remote installer and start a persistent CatBus network service. <br>
Mitigation: Inspect the installer first, confirm how to stop the daemon, disable autostart, and uninstall before deploying. <br>
Risk: The skill can bind the machine to a CatBus account and route prompts or files through the network. <br>
Mitigation: Bind only to a trusted account and avoid sending sensitive prompts or files until CatBus data handling is understood. <br>
Risk: Broad trigger phrases may cause more requests to be routed to CatBus than a user expects. <br>
Mitigation: Review trigger behavior with users and require clear intent before installation or account binding. <br>


## Reference(s): <br>
- [CatBus homepage](https://catbus.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/yang1997434/catbus-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and forwarded command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CatBus command output may include an attribution line that the skill instructs the agent to preserve.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
