## Description:

Queries and controls products and devices on the China Mobile AIoT platform (iot.10086.cn), including model data, device properties, device state changes, and video device live stream URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ch2925](https://clawhub.ai/user/ch2925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage China Mobile AIoT products and devices from an agent, including checking device status, reading properties, setting properties, invoking services, enabling or disabling devices, and retrieving live video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores CMAIoT product access keys in plaintext configuration.

Mitigation: Use least-privilege product keys, avoid entering keys on shared systems, protect the skill directory, and rotate keys after exposure.

Risk: The skill can create devices, set properties, invoke services, and enable or disable devices without built-in confirmation.

Mitigation: Require manual confirmation before create, set, call, enable, disable, or live-video actions are executed by an agent.

Risk: Credentials can be exposed through command arguments or shell history when adding a product access key.

Mitigation: Review shell history exposure, prefer controlled execution environments, and rotate any key entered on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ch2925/skills/cmaiot)
- [ClawHub publisher profile](https://clawhub.ai/user/ch2925)
- [China Mobile AIoT platform](https://iot.10086.cn)
- [CMAIoT API endpoint](https://iot-api.heclouds.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to report parsed intent, target devices, device status, operation results, and success, skipped, or failure counts.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
