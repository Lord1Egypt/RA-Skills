## Description: <br>
OpenClaw Agent 自进化记忆系统 gives OpenClaw agents persistent memory by syncing Obsidian vault content, indexing vectors, compressing session observations, and monitoring memory health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxyujian98-png](https://clawhub.ai/user/yxyujian98-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to connect Obsidian notes, session history, Qdrant, and embedding services into a persistent searchable memory system with automated sync and maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can receive recurring background access to private notes, OpenClaw session history, local memory stores, Qdrant, and model endpoints. <br>
Mitigation: Install first against a test vault, keep backups, limit synchronized directories, and review scheduled jobs before enabling broad background operation. <br>
Risk: Configured API keys and model endpoints may expose sensitive credentials or private content. <br>
Mitigation: Prefer local-only embedding and LLM endpoints where practical, store credentials outside shared files, and review configuration before use. <br>
Risk: Auto-repair behavior can mutate memory or vault content through generated repair rules. <br>
Mitigation: Do not enable auto-fix rules until the generated antibodies.json commands and maintenance scripts have been audited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxyujian98-png/agent-openclaw-memory) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown instructions with Python scripts, JSON configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Obsidian vault path, Qdrant, an embedding endpoint, and optional LLM API credentials.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
