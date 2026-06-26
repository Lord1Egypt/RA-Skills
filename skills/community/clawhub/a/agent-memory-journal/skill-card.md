## Description: <br>
Agent Memory Journal provides durable, file-based episodic and core memory for agents, with CLI and Python API workflows for recording, recalling, curating, and reviewing agent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misolith](https://clawhub.ai/user/misolith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent an inspectable local memory journal, including hot context, searchable core facts, episodic logs, session notes, and maintenance commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable local memory can retain sensitive notes, preferences, session context, or personal data longer than intended. <br>
Mitigation: Treat .memory as sensitive storage, avoid logging secrets or regulated personal data, and periodically review, delete, archive, or supersede stored memories. <br>
Risk: Hot memory and promoted core memories can influence future agent context and behavior. <br>
Mitigation: Review generated hot memory files and use explicit curation, forget, review, and doctor workflows before relying on persisted memories. <br>
Risk: A configured hot_path override can write generated memory into framework-specific files such as AGENT.md or AGENTS.md. <br>
Mitigation: Review .memory/config.json before enabling hot_path overrides and treat the configured hot target as generated output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/misolith/agent-memory-journal) <br>
- [README](artifact/README.md) <br>
- [Agent Installation Guide](artifact/docs/agent_install.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plaintext memory entries, CLI output, Python API results, and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local .memory files and may generate hot memory files such as AGENT.md according to configuration] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
