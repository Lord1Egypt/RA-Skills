## Description: <br>
Claw Memory Lite helps OpenClaw users extract, store, and query distilled long-term memory in a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timothysong0w0](https://clawhub.ai/user/timothysong0w0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index daily memory notes, query remembered facts by keyword or category, and automate local memory extraction during heartbeat or scheduled maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores distilled memory notes in a local SQLite database, which may contain sensitive information if users place secrets or private data in memory files. <br>
Mitigation: Review memory/*.md and REGRESSIONS.md before enabling extraction, keep API keys and passwords out of memory files, and delete ~/.openclaw/database/insight.db to clear stored memory. <br>
Risk: Heartbeat or cron automation can repeatedly process local memory files without an interactive review step. <br>
Mitigation: Use review mode where available before enabling scheduled extraction, and remove the scheduled heartbeat or cron command to stop automation. <br>


## Reference(s): <br>
- [Claw Memory Lite on ClawHub](https://clawhub.ai/timothysong0w0/claw-memory-lite) <br>
- [API Reference](docs/api.md) <br>
- [Installation Guide](docs/installation.md) <br>
- [Integration Guide](docs/integration.md) <br>
- [Examples](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite query results, memory extraction logs, heartbeat configuration snippets, and setup instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
