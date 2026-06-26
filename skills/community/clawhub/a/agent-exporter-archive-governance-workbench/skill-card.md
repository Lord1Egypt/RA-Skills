## Description: <br>
Use when an agent needs to wire the local agent-exporter MCP bridge, publish a local archive shell, save retrieval reports, or read governance evidence and policy packs from a repo checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a local agent-exporter stdio bridge, validate the bridge with a low-risk governance read, publish local archive shells, save retrieval reports, and inspect governance evidence from a repository checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner signals are clean, but evidence.security notes that the submitted artifact files were not available for the scanner's full content review. <br>
Mitigation: Read the skill packet before installing and confirm that its local bridge setup and requested actions match the intended use. <br>
Risk: The skill guides agents to run a local stdio bridge against repo checkouts and workspace paths. <br>
Mitigation: Start with the low-risk integration_evidence_policy_list check, use explicit local paths, and run archive or retrieval actions only on intended workspaces. <br>


## Reference(s): <br>
- [Install](references/INSTALL.md) <br>
- [Capabilities](references/CAPABILITIES.md) <br>
- [Demo](references/DEMO.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP config](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP config](references/OPENCLAW_MCP_CONFIG.json) <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/agent-exporter-archive-governance-workbench) <br>
- [agent-exporter landing page](https://xiaojiou176-open.github.io/agent-exporter/) <br>
- [Archive shell proof](https://xiaojiou176-open.github.io/agent-exporter/archive-shell-proof.html) <br>
- [Repo map](https://xiaojiou176-open.github.io/agent-exporter/repo-map/) <br>
- [agent-exporter releases](https://github.com/xiaojiou176-open/agent-exporter/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown, code] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration snippets and local file path outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local archive shell paths, retrieval report paths, governance policy lists, evidence diffs, and remediation guidance from a local repo checkout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
