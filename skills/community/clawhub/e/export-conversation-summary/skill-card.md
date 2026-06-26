## Description: <br>
Export current Claude Code conversation to markdown document with full dialogue context and model operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngbeauty](https://clawhub.ai/user/youngbeauty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to export a local conversation into a structured Markdown transcript with dialogue turns, tool-operation summaries, statistics, and evaluation notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated conversation exports can contain sensitive chat content, private code, personal data, internal file paths, command history, and session metadata. <br>
Mitigation: Review the generated Markdown before sharing, uploading, or committing it, and redact sensitive content as needed. <br>
Risk: The skill may select the wrong conversation log when multiple Claude Code sessions are active. <br>
Mitigation: Confirm the selected JSONL conversation file before exporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youngbeauty/export-conversation-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown transcript with operation summaries, conversation statistics, and evaluation sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local conversation metadata, token usage, file paths, command summaries, and preserved dialogue formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
