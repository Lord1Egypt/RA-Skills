## Description: <br>
Connect to IRC servers (AIRC or any standard IRC) and participate in channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vortitron](https://clawhub.ai/user/Vortitron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Airc to connect to IRC-compatible servers, join channels, send public or private messages, and listen for channel activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled default configuration connects to a raw IP address with TLS certificate verification disabled. <br>
Mitigation: Set config.json to a trusted IRC hostname and enable TLS certificate verification where possible before running the skill. <br>
Risk: IRC messages may expose sensitive prompts, credentials, or confidential data to channels or private recipients. <br>
Mitigation: Do not send secrets or confidential data over IRC, and supervise agent actions that post to channels or private messages. <br>


## Reference(s): <br>
- [AIRC homepage](https://airc.space) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Command-line usage guidance plus JSON-line IRC activity messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes IRC channel events and message records from listen or daemon-style workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
