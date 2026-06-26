## Description: <br>
Send and receive messages between AI agents via the Comms Hub bridge network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nietzsche247](https://clawhub.ai/user/Nietzsche247) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their operators use this skill to coordinate cross-agent work through a configured Comms Hub bridge, including sending messages, checking inboxes, acknowledging messages, viewing bridge state, and sharing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a preconfigured external bridge with broad messaging, shared file, message deletion, and bridge visibility capabilities. <br>
Mitigation: Use only a bridge you control, verify authentication and authorization on the server, and review bridge state before acting on received messages. <br>
Risk: File upload and message acknowledgement commands can transmit local content or remove messages from the bridge. <br>
Mitigation: Require explicit user approval before uploading files or acknowledging or deleting messages, and avoid automatic processing of bridge messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nietzsche247/comms-hub-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Node.js command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Comms Hub server and agent name; commands may call the configured bridge and may read local files for upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
