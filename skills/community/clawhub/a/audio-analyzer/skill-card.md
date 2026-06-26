## Description: <br>
Smart Audio Analyzer transcribes audio, identifies speakers with persistent voice profiles, detects meeting, interview, training, or talk scenes, and generates structured notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoJowillwater](https://clawhub.ai/user/JoJowillwater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and operations teams use this skill to turn permitted audio recordings into transcripts, speaker-labeled dialogue, scene-specific notes, action items, and optional local voiceprint matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive recordings and can upload audio or transcripts to cloud ASR and summarization providers. <br>
Mitigation: Use it only for recordings the user is allowed to process, disclose provider use, and prefer local Whisper for sensitive audio. <br>
Risk: Speaker embeddings and voice profile data can identify people across sessions. <br>
Mitigation: Enroll speakers only with consent, store generated profile files carefully, and delete voice-db.json and voice-profiles.md entries when no longer needed. <br>
Risk: The local Whisper fallback has a command-execution risk with untrusted filenames. <br>
Mitigation: Avoid Whisper fallback for untrusted files or unusual filenames until command construction is fixed; prefer configured cloud ASR or sanitized local paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JoJowillwater/audio-analyzer) <br>
- [Scene templates](references/scenes/) <br>
- [Voice profiles reference](references/voice-profiles.md) <br>
- [WeSpeaker model releases](https://github.com/wenet-e2e/wespeaker/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, transcript text files, optional raw JSON metadata, and command-line guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write transcripts, summaries, raw speaker metadata, voice-profiles.md updates, and local voice-db.json embeddings depending on configuration and user confirmation.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
