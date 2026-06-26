## Description: <br>
Processes Douyin video links and audio files to download media, extract audio, transcribe speech, and clean up transcript text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pry520okgpt](https://clawhub.ai/user/pry520okgpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process Douyin video links or local audio into transcripts, structured results, and saved media artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio or video may be sent to remote ASR services such as qwen-asr or Tencent Cloud. <br>
Mitigation: Use a clearly local Whisper-only configuration for private, confidential, copyrighted, or regulated media. <br>
Risk: Transcript snippets may be saved into a local memory store without clear consent, retention, or deletion controls. <br>
Mitigation: Disable or remove memory-manager writes unless consent, retention, and deletion controls are established. <br>
Risk: The skill installs dependencies and invokes external command-line tools to process user-supplied media links. <br>
Mitigation: Review the skill and dependencies before deployment and run it in a constrained environment appropriate for untrusted media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pry520okgpt/douyin-super-agent) <br>
- [Publisher profile](https://clawhub.ai/user/pry520okgpt) <br>
- [Declared homepage](https://github.com/openclaw/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcripts, JSON result files, downloaded media files, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are saved under a desktop Douyin skill directory; local Whisper model files may be cached separately.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
