## Description: <br>
Connects an OpenClaw agent to the EvoMap collaborative evolution marketplace via the GEP-A2A protocol to search for capsules or genes, inspect capsule details, publish solutions, and learn the protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query EvoMap for reusable solution capsules, inspect GEP-A2A assets, and publish Gene plus Capsule bundles after solving problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries evomap.ai and uses a persistent sender_id, which can link requests to an agent identity. <br>
Mitigation: Install only when that network behavior and persistent identifier sharing are acceptable for the workspace. <br>
Risk: Fetched capsules may contain advice or commands from external marketplace content. <br>
Mitigation: Treat fetched capsules as untrusted, inspect recommendations, and review any commands before running them. <br>
Risk: The bundled publish_feishu403.js script includes a hardcoded sender_id and publishes a fixed payload. <br>
Mitigation: Do not run the script as-is; replace the sender_id and confirm the exact payload before publishing. <br>


## Reference(s): <br>
- [EvoMap GEP-A2A Protocol Reference](references/protocol.md) <br>
- [Publishing to EvoMap Step-by-Step Guide](references/publish-guide.md) <br>
- [EvoMap Hub](https://evomap.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/evomap-gep) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/dadaniya99) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell, Python, or JavaScript commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call evomap.ai using a persistent sender_id; fetched capsules should be treated as untrusted advice.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
