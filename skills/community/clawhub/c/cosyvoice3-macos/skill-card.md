## Description: <br>
Local text-to-speech using Alibaba's CosyVoice3 on macOS Apple Silicon, with multilingual synthesis, Chinese dialect support, zero-shot voice cloning, cross-lingual synthesis, and fine-grained control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhuaizhong](https://clawhub.ai/user/lhuaizhong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to install and run a local text-to-speech workflow on macOS Apple Silicon, generate speech from text, and optionally use authorized reference audio for voice cloning or cross-lingual synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow downloads Miniconda, clones the CosyVoice repository, installs Python packages, and downloads large model files from upstream sources. <br>
Mitigation: Review scripts/install.sh before running and install only in an environment where those upstream sources and packages are trusted. <br>
Risk: Voice cloning can be misused with reference audio that the user is not authorized to use. <br>
Mitigation: Use only authorized reference audio and avoid impersonation or deceptive sharing. <br>
Risk: The workflow depends on sizeable local model files and an external ML stack. <br>
Mitigation: Confirm available disk space and dependency expectations before installation, and keep generated audio local unless it has been reviewed for the intended use. <br>


## Reference(s): <br>
- [CosyVoice GitHub](https://github.com/FunAudioLLM/CosyVoice) <br>
- [Fun-CosyVoice3 Demo](https://funaudiollm.github.io/cosyvoice3/) <br>
- [ClawHub Release Page](https://clawhub.ai/lhuaizhong/cosyvoice3-macos) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lhuaizhong) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python commands plus generated WAV audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local speech audio files after installation; requires local model files and authorized reference audio for voice cloning.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
