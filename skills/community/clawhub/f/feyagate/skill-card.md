## Description: <br>
MCP smart home gateway for AI agents. Control Xiaomi, Tuya, Midea, eWeLink, cameras, and XiaoAI speakers via MCP protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toddpan](https://clawhub.ai/user/toddpan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and smart-home operators use this skill to connect an AI agent to a local FeyaGate MCP gateway for device discovery, device control, platform authorization, scenes, schedules, cameras, speakers, and gateway administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect smart-home devices, cameras, credentials, network exposure, memory, and skill-management state. <br>
Mitigation: Review planned actions before execution, authorize only intended platforms, and avoid granting passwords, OAuth codes, API keys, camera access, endpoint changes, skill-management actions, or memory changes unless those effects are intended. <br>
Risk: Installation guidance includes remote script execution and a service that may bind beyond localhost. <br>
Mitigation: Verify the package or install script source before running it, install on a trusted machine and network, and bind the service to localhost when possible. <br>
Risk: Licensed and free-edition behavior differs across device platforms. <br>
Mitigation: Check license status before control workflows and handle license-required responses without retry loops or unintended fallback actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/toddpan/feyagate) <br>
- [Server-Resolved GitHub Provenance](https://github.com/toddpan/feyagate-skill) <br>
- [FeyaGate Homepage](https://www.feyagate.com) <br>
- [Quick Start Guide](artifact/QUICKSTART.md) <br>
- [FeyaGate MCP API](artifact/FeyaGate_MCP_API.md) <br>
- [FeyaGate HTTP API](artifact/FeyaGate_HTTP_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-RPC request examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions and tool-call arguments for a local MCP smart-home gateway; some responses may include JSON text or camera image content from the gateway.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release metadata; artifact frontmatter reports 1.2.31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
