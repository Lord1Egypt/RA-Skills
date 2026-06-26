## Description: <br>
Context Hawk provides a Python memory manager for preserving, compressing, retrieving, and injecting agent memory across sessions, topics, and long-running tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Context Hawk to add persistent memory, task-state recovery, context compression, and retrieval workflows to Python-based AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled installer paths can import existing OpenClaw memories. <br>
Mitigation: Review installer scripts before execution and avoid scripts/install.sh unless importing existing local memories is intended. <br>
Risk: Optional cloud extraction and embedding providers can send sensitive conversation or memory content outside the local environment. <br>
Mitigation: Use local or offline retrieval modes for sensitive data, and enable cloud providers only after reviewing provider configuration and data-handling requirements. <br>
Risk: The cron health-check script can automatically commit and push repository changes. <br>
Mitigation: Do not schedule the cron health-check script unless automatic git commits and pushes are acceptable for the target repository. <br>
Risk: Curl-to-bash installation can execute remote shell code before review. <br>
Mitigation: Prefer pip installation or inspect downloaded scripts before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/relunctance/context-hawk) <br>
- [README](README.md) <br>
- [Four-Tier Memory Architecture](references/memory-system.md) <br>
- [Task State Memory](references/task-state.md) <br>
- [Compression Strategies](references/compression-strategies.md) <br>
- [Context Injection Strategies](references/injection-strategies.md) <br>
- [CLI Reference](references/cli.md) <br>
- [LanceDB Integration](references/lancedb-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory files, vector indexes, task-state records, and compressed context summaries when used by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
