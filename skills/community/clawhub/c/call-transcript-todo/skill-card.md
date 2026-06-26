## Description: <br>
Transcribes call recordings into structured transcripts, concise meeting notes, extracted action items, and either a Feishu document or a local Markdown file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaishu](https://clawhub.ai/user/daaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to turn audio call recordings into readable transcripts, meeting summaries, and follow-up tasks. It is useful when a user explicitly asks to transcribe or organize a recording and wants the result saved to Feishu or Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Call recordings and derived transcripts may contain sensitive information and may be sent to Feishu automatically when credentials are configured. <br>
Mitigation: Before use, decide whether output should remain local or go to Feishu, confirm access controls for the destination, and avoid regulated or highly confidential calls unless an explicit confirmation or redaction step is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daaishu/call-transcript-todo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown transcript and summary with action items; optionally a Feishu document link or local Markdown file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append confirmed action items to memory/todo.md after user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
