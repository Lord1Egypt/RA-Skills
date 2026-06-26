## Description: <br>
Byted Las Asr Pro helps agents transcribe audio and video through Volcengine LAS, with optional diarization, language detection, emotion detection, gender detection, and async batch polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to submit audio or video transcription jobs to Volcengine LAS, estimate cost before execution, poll asynchronous jobs, and return transcripts, utterances, and recognition metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive LAS credentials and may process private media, transcripts, presigned URLs, logs, and result files. <br>
Mitigation: Use least-privilege credentials, avoid pasting long-lived secrets into chat, and treat all generated previews, links, logs, and output files as sensitive. <br>
Risk: Initialization can update or create a local virtual environment from a Volcengine-hosted SDK path. <br>
Mitigation: Install only when the Volcengine SDK download path is trusted and review environment changes before use. <br>
Risk: Detached background polling can continue after submission and may be difficult to monitor in some agent runtimes. <br>
Mitigation: Use background polling only in environments where the process can be monitored and stopped; otherwise return the task ID and poll explicitly later. <br>
Risk: Submitting transcription jobs can incur usage cost. <br>
Mitigation: Estimate price before upload or submission and require explicit user confirmation before starting a job. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-las-asr-pro) <br>
- [las_asr_pro API Reference](references/api.md) <br>
- [Pricing Reference](references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>
- [Volcengine LAS SDK Manifest](https://las-ai-cn-beijing-online.tos-cn-beijing.volces.com/operator_cards_serving/public/skills/sdk/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request templates; generated artifacts may include result JSON, transcript text, utterance JSON, and utterance CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LAS credentials and explicit user confirmation of estimated cost before submitting transcription jobs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
