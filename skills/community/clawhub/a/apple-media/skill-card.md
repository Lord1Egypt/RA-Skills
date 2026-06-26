## Description: <br>
Control Apple TV, HomePod, and AirPlay devices via pyatv (scan, stream, playback, volume, navigation). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronn](https://clawhub.ai/user/aaronn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and home media operators use this skill to discover and control Apple TV, HomePod, and AirPlay devices from an agent through pyatv and atvremote commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pairing stores reusable local credentials in ~/.pyatv.conf. <br>
Mitigation: Protect the credentials file and remove it when the machine or agent environment is no longer trusted. <br>
Risk: Agent-issued playback, volume, navigation, power, and streaming commands can affect local Apple media devices. <br>
Mitigation: Review target device names, files, URLs, and command intent before execution. <br>
Risk: The documented install path depends on pyatv compatibility with Python 3.13 or earlier. <br>
Mitigation: Install pyatv with the documented Python 3.13 pipx command when newer Python runtimes are the default. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/aaronn/apple-media) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require the atvremote binary and access to the target local-network media device.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
