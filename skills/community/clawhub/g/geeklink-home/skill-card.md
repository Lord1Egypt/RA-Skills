## Description: <br>
Geeklink Home controls local gateway devices and scenes over LAN, supporting device and scene listing, state checks, scene activation, and device control with pairing-token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lintertion](https://clawhub.ai/user/lintertion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home users use this skill to let an agent discover and control Geeklink Home gateway devices and scenes on a trusted local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway credentials are cached locally in plaintext. <br>
Mitigation: Use only on a trusted machine and trusted LAN, protect the pairing token like a password, and inspect or remove ~/.geeklink-home/config.json when cached access is no longer wanted. <br>
Risk: The skill can change connected device and scene state. <br>
Mitigation: Review the selected device or scene before running control commands, and list devices first when the natural-language mapping is unclear. <br>
Risk: The loaded runtime can monitor recent smart-home events. <br>
Mitigation: Use the watcher only where event monitoring is expected, and remove cached access when persistent monitoring is no longer appropriate. <br>


## Reference(s): <br>
- [Geeklink Home ClawHub page](https://clawhub.ai/lintertion/geeklink-home) <br>
- [lintertion publisher profile](https://clawhub.ai/user/lintertion) <br>
- [Geeklink Home Gateway Template](references/gateway_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; command results may include device, scene, state, and event text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and local Geeklink gateway access with a pairing token.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence, _meta.json, PUBLISH.md, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
