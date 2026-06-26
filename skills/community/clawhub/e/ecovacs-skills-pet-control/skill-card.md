## Description: <br>
Controls Ecovacs FAMIBOT pet robots through the Ecovacs Open Platform Access Key for device discovery, state queries, settings, sounds, motion actions, sleep, reset, and the showcase_custom dance preset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ecovacs-ai](https://clawhub.ai/user/ecovacs-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and integrators use this skill to let an assistant operate supported Ecovacs FAMIBOT pet robots with an Open Platform AK. It supports checking robot state, adjusting everyday device settings, playing built-in sounds, and running bounded motion or dance routines. <br>

### Deployment Geography for Use: <br>
Global, with Mainland China as the default gateway and a non-China gateway override documented by the skill. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change privacy-sensitive robot settings, including camera, microphone, wake word, nickname, sleep, and reset behavior. <br>
Mitigation: Use explicit confirmation before sensitive settings or disruptive actions, and restrict use to trusted publishers and trusted operators. <br>
Risk: Motion commands may automatically wake the robot by enabling camera before running visible actions. <br>
Mitigation: Tell users when a motion request may wake the robot or enable camera, and allow them to cancel before execution. <br>
Risk: The Access Key can be exposed through URLs, shell history, or the local session file. <br>
Mitigation: Prefer environment variables or protected local storage, avoid placing the AK in URLs or saved command history, and remove or protect ~/.ecovacs_session.json when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ecovacs-ai/ecovacs-skills-pet-control) <br>
- [Ecovacs Open Platform (Mainland China)](https://open.ecovacs.cn/) <br>
- [Ecovacs Open Platform (non-China regions)](https://open.ecovacs.com/) <br>
- [API reference](references/api.md) <br>
- [Schema notes](references/schema.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Single-action protocol](references/phoenix-single-action.md) <br>
- [Action-sequence protocol](references/phoenix-action-control.md) <br>
- [Action sequence timing](references/action-sequence.md) <br>
- [Dance routines](references/dance-routines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON payloads] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Ecovacs Open Platform AK and a device nickname fragment; responses depend on robot model, firmware, deployment, and online status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
