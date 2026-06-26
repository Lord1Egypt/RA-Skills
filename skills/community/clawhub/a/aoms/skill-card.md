## Description: <br>
AOMS is a persistent local memory service for AI agents with episodic, semantic, procedural, and working memory, weighted retrieval, optional vector search, progressive disclosure, and automatic weight decay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DhawalA4](https://clawhub.ai/user/DhawalA4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use AOMS to give agents persistent local memory across sessions, recall relevant task context, store learned facts and workflows, and integrate memory with OpenClaw, Claude Code, Codex, or HTTP-capable agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-term local agent memory that may contain sensitive or regulated information. <br>
Mitigation: Avoid storing secrets or regulated data, choose an appropriate local storage root, and review retained memories periodically. <br>
Risk: The local HTTP memory service could expose memory contents if bound beyond localhost or run without host-level controls. <br>
Mitigation: Keep the service bound to localhost unless a reviewed deployment plan requires otherwise, and protect the host with normal local access controls. <br>
Risk: Recalled memory can influence future prompts and may introduce stale, incorrect, or unsafe context. <br>
Mitigation: Review recalled memory before injecting it into prompts and reinforce or decay memories based on observed usefulness. <br>
Risk: Workspace migration can import unintended Markdown content into persistent memory. <br>
Mitigation: Run migration in dry-run mode first, review the files and proposed entries, and import only when the scope is intentional. <br>
Risk: Running the package or container as an always-on daemon increases supply-chain and operational exposure. <br>
Mitigation: Verify the cortex-mem package or container before daemonizing it and keep the installation updated through the intended package channel. <br>


## Reference(s): <br>
- [AOMS API Reference](references/api-reference.md) <br>
- [OpenClaw Setup](references/openclaw-setup.md) <br>
- [ClawHub Release Page](https://clawhub.ai/DhawalA4/aoms) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, JSON, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local HTTP API usage, daemon setup, OpenClaw configuration, and prompt-ready memory recall patterns.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
