## Description: <br>
Agent Memory Cleanup audits and cleans long-term agent memory files, preserving durable user context while removing stale task notes, duplicates, conflicts, and suspected secrets after approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to audit, prune, sanitize, deduplicate, and repair long-term memory files for Codex, OpenClaw, Hermes Agent, Claude, and similar runtimes. It helps agents keep stable global preferences while removing task-specific residue, stale project notes, contradictions, and suspected credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads long-term memory files that may contain private user context or sensitive credentials. <br>
Mitigation: Use it only for intended memory cleanup, keep reports local when possible, and rely on the skill's redaction behavior before sharing findings. <br>
Risk: Approved cleanup can modify memory files or write proposed reports to paths chosen by the user. <br>
Mitigation: Review proposed diffs before applying, keep timestamped backups until satisfied, and avoid output paths that could expose memory reports or overwrite unrelated files. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/hollis9087/agent-memory-cleanup) <br>
- [README](README.md) <br>
- [Default Cleanup Rules](references/default-rules.json) <br>
- [Classification Rubric](references/classification-rubric.md) <br>
- [Agent Memory Paths](references/agent-paths.md) <br>
- [MCP Version Guidance](references/mcp-version.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, File edits, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON summaries, diffs, shell commands, and approved memory-file edits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped backups before approved edits and redacts suspected secrets in reports.] <br>

## Skill Version(s): <br>
0.3.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
