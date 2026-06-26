## Description: <br>
Markdown-based memory continuity system for agents that use local Markdown files for daily logs, project memory, handoff notes, state records, session protocols, and OpenClaw memory-tool workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[durugy](https://clawhub.ai/user/durugy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Duru Memory to maintain Markdown-backed long-term memory, retrieve context, run session start and close routines, and manage memory retention in OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can modify files beyond the intended memory area if installed or invoked without workspace review. <br>
Mitigation: Review or patch helper scripts before installation and constrain writes and tagging to workspace memory files. <br>
Risk: Memory content can be sent to a configurable model endpoint for tagging, compaction, or semantic retrieval. <br>
Mitigation: Keep Ollama configured to localhost unless remote processing is intentional, avoid storing secrets in memory files, and periodically review or delete persisted memory and semantic indexes. <br>


## Reference(s): <br>
- [Memory File Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, configuration steps, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Markdown memory files and maintain a local semantic index when helper scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
