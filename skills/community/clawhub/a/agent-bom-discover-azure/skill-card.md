## Description: <br>
Discover Azure-hosted AI agent and MCP-relevant assets from the operator's environment, emit canonical agent-bom inventory JSON, and scan it without giving agent-bom long-lived Azure credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security teams use this skill to inventory Azure OpenAI, Container Apps, AKS, Functions, ML, and related agentic Azure infrastructure as canonical agent-bom inventory. The skill is intended for operator-approved, read-only discovery followed by optional local scanning when findings are requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inventories Azure resources and may expose sensitive environment or infrastructure details in generated inventory files. <br>
Mitigation: Use a least-privilege read-only Azure identity, write inventory only to an operator-selected path, and review generated JSON before sharing it. <br>
Risk: Azure credential material could be exposed if operators paste secrets into chat or logs. <br>
Mitigation: Use the existing Azure identity chain where possible and avoid pasting client secrets, access tokens, or connection strings. <br>
Risk: The skill depends on the separately installed agent-bom package or repository, which is not bundled in this artifact. <br>
Mitigation: Evaluate the installed agent-bom package or repository independently before running scans. <br>


## Reference(s): <br>
- [agent-bom repository](https://github.com/msaad00/agent-bom) <br>
- [agent-bom PyPI project](https://pypi.org/project/agent-bom/) <br>
- [ClawHub skill page](https://clawhub.ai/msaad00/agent-bom-discover-azure) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON inventory outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-selected inventory JSON and optional agent-bom findings JSON.] <br>

## Skill Version(s): <br>
0.89.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
