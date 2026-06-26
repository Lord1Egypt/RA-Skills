## Description: <br>
Local speech-to-text using faster-whisper with GPU acceleration support, word-level timestamps, and distilled model options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Damirikys](https://clawhub.ai/user/Damirikys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files into text or structured JSON, with options for model choice, language, word timestamps, voice activity detection, and CPU or CUDA execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script downloads Python packages and may download speech models on first use. <br>
Mitigation: Review setup.sh before installation, run it without elevated privileges, and install only in environments where those package and model downloads are acceptable. <br>
Risk: Audio files and generated transcripts can contain private or sensitive information. <br>
Mitigation: Keep audio and transcript files in approved local storage and apply the user's normal data handling requirements before sharing or retaining outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Damirikys/faster-whisper-local) <br>
- [PyTorch CUDA wheel index](https://download.pytorch.org/whl/cu121) <br>
- [PyTorch package index](https://download.pytorch.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Plain text transcript or JSON containing transcript text, detected language, duration, segments, and optional word timestamps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write output to a file; supports model, language, beam size, voice activity detection, device, compute type, quiet mode, and first-run model downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
