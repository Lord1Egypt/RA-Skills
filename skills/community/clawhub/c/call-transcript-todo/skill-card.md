## Description:

Call-Transcript-Todo transcribes call audio into structured Chinese-oriented notes with a transcript, summary, and extracted follow-up tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaishu](https://clawhub.ai/user/daaishu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to process call recordings when the user explicitly asks for transcription or meeting-note cleanup. It converts supported audio files into a readable transcript, a concise summary, follow-up tasks, and either a Feishu document or a local Markdown file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may modify the active Python environment broadly.

Mitigation: Install and run the skill in an isolated environment or virtualenv, and pin and verify dependencies before use.

Risk: Feishu credentials enable document creation in the configured workspace.

Mitigation: Provide FEISHU_APP_ID and FEISHU_APP_SECRET only when Feishu output is intended, and use the least-privileged app credentials available.

Risk: The default transcription and output flow is Chinese-oriented and may not fit all audio languages or note formats.

Mitigation: Confirm that Chinese transcription and the generated note structure match the intended workflow before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daaishu/skills/call-transcript-todo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, Feishu document content, local Markdown files, and concise user guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown output and append confirmed tasks to memory/todo.md; may create a Feishu document when credentials are configured.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
