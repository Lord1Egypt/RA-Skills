## Description: <br>
Searches the e-store marketplace so an agent can browse, download, configure, and install AI skills, MCP servers, tools, assets, knowledge resources, and bundled solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iuliganma](https://clawhub.ai/user/iuliganma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a task requires acquiring a new capability, asset, knowledge source, or prebuilt solution from e-store instead of building it from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to contact e-store and install third-party capabilities with broad local effects. <br>
Mitigation: Require explicit user confirmation before any download, configuration write, skill or MCP installation, or host reload. <br>
Risk: The documented API uses E_STORE_AK in request URLs, which can expose the access key through logs, shell history, or copied links. <br>
Mitigation: Treat E_STORE_AK as a secret, avoid printing full authenticated URLs, and redact the key from logs and shared output. <br>
Risk: Downloaded resources, bundles, or configuration text may introduce unreviewed third-party behavior. <br>
Mitigation: Inspect and scan downloaded artifacts or generated configuration before enabling them in the agent runtime. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/iuliganma/e-store-skill) <br>
- [e-store marketplace](https://store.liganma.com) <br>
- [e-store skill detail](https://store.liganma.com/detail?id=1248353041200058368) <br>
- [e-store Access API reference](references/API.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to e-store and an E_STORE_AK secret for authenticated API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact metadata version 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
