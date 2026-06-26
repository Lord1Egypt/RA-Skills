## Description: <br>
Structured episodic, semantic, and procedural memory framework for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DurtyDhiana](https://clawhub.ai/user/DurtyDhiana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create local memory folders, templates, and routines that preserve episodic logs, durable knowledge, procedures, feedback, and post-compaction context. It also provides shell-based search guidance for recalling tagged decisions, procedures, blockers, and recent activity from memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may accumulate sensitive project data, personal information, credentials, or internal endpoints. <br>
Mitigation: Treat the memory folder like sensitive project data; avoid storing passwords, API keys, tokens, private keys, auth headers, and unnecessary personal information, and redact internal endpoints where possible. <br>
Risk: Search output may reveal sensitive information from durable memory files if copied into prompts, logs, or shared reports. <br>
Mitigation: Review search results before sharing them outside the workspace and prune or archive stale memory files periodically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DurtyDhiana/agent-memory-kit-2-1-0) <br>
- [README](README.md) <br>
- [Search and Recall Guide](SEARCH.md) <br>
- [Installation Guide](INSTALLATION.md) <br>
- [Search Quick Start](QUICKSTART-SEARCH.md) <br>
- [Search Installation Guide](INSTALL-SEARCH.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and reusable templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory structures, logging templates, wake routine guidance, and search command patterns for agent workflows.] <br>

## Skill Version(s): <br>
2.1.0 (source: artifact/_meta.json and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
