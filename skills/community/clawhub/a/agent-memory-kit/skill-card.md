## Description: <br>
Provides a structured memory system for AI agents that separates episodic, semantic, and procedural memories so agents can preserve knowledge and processes over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancampbell](https://clawhub.ai/user/ryancampbell) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add local long-term memory practices, templates, and search workflows to an AI agent workspace. It helps agents record daily context, durable knowledge, procedures, feedback, and compaction recovery notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files may capture private notes, sensitive procedures, personal data, passwords, or tokens if users copy raw context into them. <br>
Mitigation: Treat memory files as private workspace notes and avoid storing secrets, raw conversations, personal data, or sensitive internal procedures. <br>
Risk: The documentation includes shell commands for setup, PATH changes, copying files, and removing search files. <br>
Mitigation: Review shell commands before running them, especially PATH changes and any rm commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryancampbell/agent-memory-kit) <br>
- [README](README.md) <br>
- [Search documentation](SEARCH.md) <br>
- [Installation guide](INSTALLATION.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands and reusable memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace memory templates and search guidance; no remote service output is required.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and changelog, released 2026-02-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
