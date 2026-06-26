## Description: <br>
Provides a three-layer persistent memory framework for agents, covering daily notes, distilled long-term memory, and archived memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azhong517-svg](https://clawhub.ai/user/azhong517-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local persistent memory conventions to an agent workspace, including daily logs, distilled long-term memory, and archival maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may contain private user or project context. <br>
Mitigation: Keep MEMORY.md, memory/*.md, and archives private; do not store secrets; and do not load them in shared sessions. <br>
Risk: The skill can lead agents to change future behavior through AGENTS.md, TOOLS.md, skill, or cron-job edits. <br>
Mitigation: Review proposed configuration, skill, and cron edits before allowing them. <br>
Risk: Archived and long-term memory can retain stale or sensitive dynamic information. <br>
Mitigation: Review outdated dynamic information during maintenance and archive or remove it when it no longer belongs in active memory. <br>


## Reference(s): <br>
- [Memory System Conventions](references/conventions.md) <br>
- [Distillation Process](references/distillation.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local MEMORY.md and memory/*.md conventions; no external API calls are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
