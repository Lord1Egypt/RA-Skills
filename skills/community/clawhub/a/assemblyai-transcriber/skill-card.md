## Description: <br>
Transcribe audio files with speaker diarization, automatic language detection, timestamps, and support for common audio formats using AssemblyAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe meetings, interviews, podcasts, voice messages, or audio URLs into readable transcripts with speaker labels and timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local audio files or audio URLs are sent to AssemblyAI for cloud transcription under the user's API key. <br>
Mitigation: Use only recordings you are authorized to process, avoid confidential or regulated audio unless approved, and review AssemblyAI privacy, retention, compliance, and billing terms before use. <br>
Risk: The AssemblyAI API key can be exposed if stored or shared carelessly. <br>
Mitigation: Prefer ASSEMBLYAI_API_KEY or a protected local config file and avoid committing API keys to shared workspaces or repositories. <br>


## Reference(s): <br>
- [AssemblyAI Website](https://www.assemblyai.com/) <br>
- [AssemblyAI API Endpoint](https://api.assemblyai.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown transcript by default, or raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASSEMBLYAI_API_KEY and sends selected local audio files or audio URLs to AssemblyAI for transcription.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md author footer) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
