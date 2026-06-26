## Description: <br>
会议纪要生成器 - 自动将会议录音转为结构化纪要 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to turn meeting recordings into structured notes with summaries, action items, decisions, and todos. It supports single-file and batch processing workflows for common audio and video recording formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings, transcripts, and generated prompts are sent to OpenAI for transcription and summarization. <br>
Mitigation: Install and use the skill only when the relevant data handling policy permits this processing, and avoid sensitive or regulated meetings unless approved. <br>
Risk: Credential and cleanup paths may be confusing because the skill supports both shell-provided OPENAI_API_KEY values and a generated .env file, and stores backup or log directories under the skill parent. <br>
Mitigation: Set OPENAI_API_KEY explicitly in the shell when possible, run the skill on narrow folders, and manually check the skill directory and parent for .env, .ai_meeting_backup, and .ai_meeting_logs during cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/ai-meeting-helper) <br>
- [Publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown, plain text, JSON, or preview text printed to the terminal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include meeting summaries, action items, decisions, todos, and optional backup files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
