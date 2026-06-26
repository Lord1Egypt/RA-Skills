## Description: <br>
Two-tier memory system for OpenClaw agents that combines recent QMD semantic search with long-term SQLite archival and optional Ollama-based summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpmoregain-eth](https://clawhub.ai/user/jpmoregain-eth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep recent OpenClaw memories searchable while moving older memory files into a long-term SQLite archive. It supports manual archive runs, cron-based archiving, archive search, and a Python interface for querying recent and archived sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The archiver can process and retain sensitive OpenClaw memory data in long-term SQLite storage. <br>
Mitigation: Install it only when long-term memory retention is intended; run --dry-run first and review the files that would be archived. <br>
Risk: LLM summarization sends memory content to the configured Ollama runtime during archive creation. <br>
Mitigation: Use --skip-llm for sensitive workspaces or confirm that Ollama is local and trusted before enabling summarization. <br>
Risk: Cron-based archiving can automatically move old memory files into the archive directory and database. <br>
Mitigation: Review the retention threshold, database path, and archive directory before installing the cron job. <br>
Risk: The README includes a curl-to-shell Ollama installation example. <br>
Mitigation: Use a verified Ollama installation method rather than running remote installer commands blindly. <br>


## Reference(s): <br>
- [QMD Setup Guide](references/qmd-setup.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Ollama Download](https://ollama.com/download) <br>
- [PyTorch CUDA Wheels](https://download.pytorch.org/whl/cu121) <br>
- [ClawHub Skill Page](https://clawhub.ai/jpmoregain-eth/agent-tiered-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, Python scripts, shell commands, configuration snippets, CLI text output, and SQLite archive records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are returned as recent-file matches and archived-session summaries; archiving can run with Ollama summarization or fallback summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
