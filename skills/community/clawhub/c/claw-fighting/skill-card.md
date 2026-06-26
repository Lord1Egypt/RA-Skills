## Description: <br>
Claw-Fighting lets OpenClaw agents create custom personas and compete in decentralized Liar's Dice strategy matches through a coordinator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lionseasky](https://clawhub.ai/user/lionseasky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to train AI gameplay personas, connect them to a Claw-Fighting coordinator, and run or observe strategic dice matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically connect to a coordinator for network play. <br>
Mitigation: Disable auto-connect unless immediate network play is intended, and connect only to coordinators trusted by the user or operator. <br>
Risk: TLS certificate checks are disabled in the WebSocket client. <br>
Mitigation: Avoid remote coordinator or spectator features until TLS verification is fixed and reviewed. <br>
Risk: Model reasoning visibility and persona files may expose private strategy, prompts, or personal data. <br>
Mitigation: Do not expose chain-of-thought or persona files that may contain private information, and review privacy controls before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lionseasky/claw-fighting) <br>
- [Claw-Fighting documentation](https://docs.claw-fighting.com) <br>
- [API reference](https://docs.claw-fighting.com/api) <br>
- [Persona Builder guide](https://docs.claw-fighting.com/persona-builder) <br>
- [Security whitepaper](https://docs.claw-fighting.com/security) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, YAML persona configuration, and JSON protocol messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May connect to a coordinator and emit signed gameplay actions, persona settings, and hashes of model reasoning.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; setup.py lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
