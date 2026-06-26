## Description: <br>
Persistent conversation export and replay for AI agent sessions across Claude Code, Caveman, OpenClaw, Hermes, MCP agents, and multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laohu-aiskills](https://clawhub.ai/user/laohu-aiskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to export, save, archive, snapshot, serialize, or back up AI agent conversations. It supports human-readable review, RAG ingestion, JSONL dataset creation, observability, and replay-oriented debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported archives may contain secrets, personal data, local file paths, proprietary code, or tool outputs from the original agent session. <br>
Mitigation: Review and redact exported files before sharing, committing, backing up, indexing, or using them for datasets; choose the narrowest export mode that fits the task. <br>
Risk: Full and replay-oriented exports can preserve detailed tool results and workflow history that may be sensitive. <br>
Mitigation: Use compact or manually redacted exports for sensitive sessions and restrict archive storage to locations appropriate for the data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laohu-aiskills/agent-archive) <br>
- [Output template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSONL, Guidance] <br>
**Output Format:** [Markdown or JSONL archive files with session metadata, tool-call details, chunks, and replay structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports compact, full, rag, replay, and jsonl export modes; long sessions may include a table of contents, summaries, and chunks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
