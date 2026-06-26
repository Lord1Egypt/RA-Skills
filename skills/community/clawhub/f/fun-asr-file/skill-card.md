## Description: <br>
Transcribes local audio files with Alibaba Cloud DashScope FunASR using non-streaming speech-to-text and local file handling optimized for common audio formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenggongdu](https://clawhub.ai/user/chenggongdu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe user-selected local audio files, including common formats such as WAV, MP3, M4A, FLAC, and OGG. It is suited to batch or file-based speech-to-text workflows where selected audio may be sent to Alibaba Cloud DashScope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to Alibaba Cloud DashScope for transcription. <br>
Mitigation: Use only audio the user is authorized to transcribe, avoid sensitive recordings unless approved, and disclose the external service dependency before use. <br>
Risk: The skill depends on a DashScope API key and third-party Python dependencies. <br>
Mitigation: Use a dedicated, rotatable DASHSCOPE_API_KEY and install dependencies from trusted package sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenggongdu/fun-asr-file) <br>
- [Publisher Profile](https://clawhub.ai/user/chenggongdu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript output with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; FFmpeg is recommended for local audio conversion to 16 kHz mono WAV.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
