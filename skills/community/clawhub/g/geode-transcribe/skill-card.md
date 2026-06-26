## Description: <br>
Transcribe and summarize audio/video files locally. Unlimited usage at a flat rate for heavy users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geodeteam](https://clawhub.ai/user/geodeteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to submit audio or video files to Geode.app for local macOS transcription, optional summarization, and asynchronous result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive audio, transcripts, summaries, and task metadata are stored locally in Geode's shared App Group container. <br>
Mitigation: Use the skill only with trusted local files, avoid processing highly sensitive recordings unless storage is acceptable, and periodically delete completed task artifacts from the shared folders. <br>
Risk: Command inputs such as file paths and language choices affect local CLI execution and transcription behavior. <br>
Mitigation: Confirm the exact file path, intended language, and summarization setting before submission, and avoid unusual characters in paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geodeteam/geode-transcribe) <br>
- [Geode App Store listing](https://apps.apple.com/app/apple-store/id6752685916?pt=127800752&ct=openclaw&mt=8) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, task IDs, JSON task status, and transcript or summary file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local file paths in Geode's shared App Group container and optional summary files when summarization is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
