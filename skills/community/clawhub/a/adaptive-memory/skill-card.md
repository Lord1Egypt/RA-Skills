## Description: <br>
Hierarchical memory management for AI agents across sessions, using daily notes, active context, and long-term memory with periodic distillation from raw notes to curated memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yozu](https://clawhub.ai/user/yozu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up durable workspace memory, decide what should be captured, and consolidate daily notes into long-term context across sessions or compaction boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files can accidentally retain secrets, tokens, passwords, or sensitive client data. <br>
Mitigation: Do not write secrets to memory files; reference secure file paths instead and treat memory files as potentially shared or version-controlled. <br>
Risk: Automatic distillation or pruning can preserve incorrect context or remove useful history. <br>
Mitigation: Review proposed memory updates before relying on them, and use version control or backups for workspaces where memory files are important. <br>


## Reference(s): <br>
- [Distillation Guide](references/distillation-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/yozu/adaptive-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace memory files and maintenance guidance; no network output is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
