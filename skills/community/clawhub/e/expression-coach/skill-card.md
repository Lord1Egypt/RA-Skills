## Description: <br>
Expression Coach is a voice-first speaking coach for Chinese communication practice, using Whisper transcription to score impromptu speaking, role-play workplace and social scenarios, suggest expression frameworks, track progress, and optionally save practice data to Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndreLYL](https://clawhub.ai/user/AndreLYL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and individual learners use this skill to practice spoken workplace and social communication through voice prompts, AI feedback, role-play simulation, reusable speaking frameworks, progress reports, and daily practice tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice recordings, transcripts, scores, and coaching notes may contain personal, workplace, or sensitive conversation data. <br>
Mitigation: Use the skill only with informed users, avoid raw-audio retention unless needed, and review/delete saved records regularly. <br>
Risk: Optional Feishu Bitable tracking can persist practice data and voice attachments outside the chat session. <br>
Mitigation: Use a dedicated limited-access Bitable app and table, limit permissions, and confirm how users can pause logging or delete records. <br>
Risk: Daily tips can create scheduled outbound messages after setup. <br>
Mitigation: Keep daily tips disabled unless explicitly configured, document the target channel, and provide a clear way to disable the cron job. <br>
Risk: Whisper transcription and speech-analysis feedback can misread pauses, filler words, or intent. <br>
Mitigation: Treat scores and coaching feedback as practice guidance, not definitive assessment, and allow users to review or correct transcripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AndreLYL/expression-coach) <br>
- [README](README.md) <br>
- [Expression frameworks](references/frameworks.md) <br>
- [Scenario library](references/scenarios.md) <br>
- [Impromptu topic library](references/topics.md) <br>
- [Daily expression tips](references/daily-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and chat text with scoring tables, speech-analysis feedback, role-play turns, progress reports, JSON configuration examples, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration and tip state, and may save transcripts, scores, analysis, and optional voice attachments to Feishu Bitable when tracking is enabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
