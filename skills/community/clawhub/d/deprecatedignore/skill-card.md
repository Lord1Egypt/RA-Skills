## Description: <br>
Connects voice transcripts and agent responses through the hotbutter.ai hosted relay for remote voice interaction with OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michael-stajer](https://clawhub.ai/user/michael-stajer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect browser-based voice interaction to a local OpenClaw agent through a hosted or configured WebSocket relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken transcripts and agent responses pass through the hosted hotbutter.ai relay by default. <br>
Mitigation: Use `--relay-url` with a relay you control, or avoid sessions where relay transit is unacceptable. <br>
Risk: Local agent output may include secrets or private data that would be sent through the relay. <br>
Mitigation: Avoid running agents that print sensitive information while using this skill. <br>
Risk: The optional first-run email and configuration are stored locally in `~/.hotbutter`. <br>
Mitigation: Remove or protect `~/.hotbutter` if the retained local configuration is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michael-stajer/deprecatedignore) <br>
- [hotbutter.ai hosted relay](https://hotbutter.ai) <br>
- [hotbutter-os local alternative](https://github.com/hotbutter-ai/hotbutter-os) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal output and relayed text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw CLI and a relay URL; defaults to wss://hotbutter.ai.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
