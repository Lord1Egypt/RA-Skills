## Description: <br>
Fun-ASR-Nano transcribes local audio files with sherpa-onnx and a ModelScope-hosted speech recognition model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengzhendong](https://clawhub.ai/user/pengzhendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and end users use this skill to transcribe user-provided audio files into text. It is suited for local speech-to-text workflows that need support for Chinese dialects, English, Japanese, lyrics, and rap speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime model download may require network access and local model caching despite offline-use claims. <br>
Mitigation: Install only when first-run or runtime ModelScope downloads are acceptable; for sensitive or air-gapped use, pre-stage the model and document the cache path. <br>
Risk: Model files are downloaded at runtime without evidence of pinned versions or integrity verification. <br>
Mitigation: Prefer a release that pins model versions and verifies model integrity before loading cached files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pengzhendong/fun-asr-nano) <br>
- [Publisher profile](https://clawhub.ai/user/pengzhendong) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript output with optional timestamp lines and supporting Markdown command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one or more local audio file paths; CLI options control language, device provider, prompts, decoding settings, hotwords, and inverse text normalization.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
