## Description: <br>
Agent Link Relay Server helps developers deploy and configure a Python WebSocket relay for cross-device OpenClaw agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericshpych](https://clawhub.ai/user/ericshpych) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy a relay server and configure agents so OpenClaw instances on different machines can exchange messages through the relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent messages can be relayed over plaintext WebSockets if deployed with ws://. <br>
Mitigation: Use WSS/TLS for non-local connections and avoid sending confidential prompts, credentials, or sensitive payloads through the relay. <br>
Risk: The relay uses a shared secret across participating agents and instances. <br>
Mitigation: Generate a strong secret, store it outside version control, rotate it regularly, and limit relay access to trusted infrastructure. <br>
Risk: The public_key configuration field may imply stronger protection than the implementation provides. <br>
Mitigation: Do not rely on public_key for signature verification or encryption unless the implementation is updated to enforce it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ericshpych/agent-link-relay-server) <br>
- [Publisher profile](https://clawhub.ai/user/ericshpych) <br>
- [README](README.md) <br>
- [Relay installation guide](docs/install-relay.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, Python, shell, and systemd examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance and configuration examples for a relay server; the bundled Python script runs a WebSocket relay when installed separately.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
