## Description: <br>
Discovers Azure-hosted AI agent and MCP-relevant assets from the operator's environment, emits canonical agent-bom inventory JSON, and scans it only when requested without giving agent-bom long-lived Azure credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security or operations engineers use this skill to inventory Azure OpenAI, Container Apps, AKS, Functions, ML, and agentic Azure infrastructure as canonical agent-bom inventory, then optionally run an agent-bom scan for findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure inventory can reveal resource names, architecture, permissions, and service metadata even when credentials are redacted. <br>
Mitigation: Review generated inventory before sharing it, store it only in operator-approved locations, and limit access to teams that need the cloud asset details. <br>
Risk: Azure credential material or secrets could be exposed if an operator pastes, logs, or exports raw identity values. <br>
Mitigation: Use least-privilege read-only Azure identities, prefer Azure CLI, workload identity, managed identity, or short-lived service principals, and do not print or request raw secrets or tokens. <br>
Risk: Running discovery against the wrong subscription could capture unintended cloud inventory. <br>
Mitigation: Require operator-approved subscriptions and an explicit output path, and keep the workflow discovery-only with no Azure resource modification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msaad00/skills/agent-bom-discover-azure) <br>
- [agent-bom project homepage](https://github.com/msaad00/agent-bom) <br>
- [agent-bom PyPI package](https://pypi.org/project/agent-bom/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and local JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-selected Azure inventory JSON and optional agent-bom findings JSON; credentials remain in the operator environment.] <br>

## Skill Version(s): <br>
0.91.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
