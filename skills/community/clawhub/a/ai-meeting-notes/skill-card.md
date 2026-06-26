## Description: <br>
AI Meeting Notes turns pasted meeting notes, transcripts, and other unstructured text into summaries, action items with owners and deadlines, saved meeting-note files, and optional to-do tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffjhunter](https://clawhub.ai/user/jeffjhunter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, consultants, and other knowledge workers use this skill to convert pasted notes, transcripts, email threads, and chat excerpts into concise meeting summaries, numbered action items, decisions, and follow-up prompts. It also helps maintain a local Markdown to-do list from selected meeting action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted notes, transcripts, and raw original text may persist in workspace files. <br>
Mitigation: Use the skill in a private workspace, redact sensitive content before processing when needed, and periodically review or delete saved meeting notes. <br>
Risk: Selected action items may be written to todo.md and remain visible in the workspace. <br>
Mitigation: Review todo.md after updates and remove completed, sensitive, or no-longer-needed items. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeffjhunter/ai-meeting-notes) <br>
- [Publisher Homepage](https://jeffjhunter.com) <br>
- [Output Example](artifact/examples/output-example.md) <br>
- [Preferences Template](artifact/assets/PREFERENCES-template.md) <br>
- [To-Do Template](artifact/assets/TODO-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Single-message meeting summary with numbered action items, plus saved Markdown files and optional JSON, table, Slack, or email variants.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default workflow saves full meeting notes under meeting-notes/ and selected action items in todo.md.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
