## Description:

Wires a local agent-exporter stdio MCP bridge so an agent can publish local archive shells, save retrieval reports, and read governance evidence and policy packs from a repository checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect a local agent-exporter checkout to a host, prove the bridge with a low-risk governance read, publish archive shells, run semantic or hybrid retrieval, and inspect governance evidence without treating the workflow as a hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the host to run an external, unpinned MCP bridge from a local checkout that is not included in the reviewed artifact.

Mitigation: Review the exact agent-exporter checkout before installing, prefer an official immutable release or commit, and only wire the MCP config to a bridge path you trust.

Risk: The bridge may receive workspace and host access through the local MCP configuration.

Mitigation: Run the bridge with the narrowest workspace and host permissions available, and start with the low-risk integration_evidence_policy_list check before archive or retrieval work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/skills/agent-exporter-archive-governance-workbench)
- [Publisher Profile](https://clawhub.ai/user/xiaojiou176)
- [agent-exporter Landing](https://xiaojiou176-open.github.io/agent-exporter/)
- [Archive Shell Proof](https://xiaojiou176-open.github.io/agent-exporter/archive-shell-proof.html)
- [Repo Map](https://xiaojiou176-open.github.io/agent-exporter/repo-map/)
- [agent-exporter Releases](https://github.com/xiaojiou176-open/agent-exporter/releases)
- [Install](references/INSTALL.md)
- [Capabilities](references/CAPABILITIES.md)
- [Demo](references/DEMO.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool names, file paths, shell commands, and JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file paths, MCP wiring steps, retrieval report guidance, and governance evidence summaries.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
