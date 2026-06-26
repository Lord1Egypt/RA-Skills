## Description: <br>
Fish Audio S2 Pro TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy and operate Fish Audio S2 Pro for multilingual text-to-speech, voice cloning, streaming audio generation, batch synthesis, and LoRA fine-tuning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation and execution of external Fish Audio packages, containers, and model weights. <br>
Mitigation: Use an isolated environment, review external dependencies before execution, and run containers or servers with least-privilege access. <br>
Risk: API server examples can expose text-to-speech and voice-cloning functionality if bound beyond localhost. <br>
Mitigation: Keep services bound to localhost unless access controls, authentication, and network restrictions are configured. <br>
Risk: Reference audio inputs can include URLs, base64 data, or file paths that may contain sensitive or untrusted voice data. <br>
Mitigation: Avoid untrusted ref_audio URLs and file:// inputs, and only process voice samples from trusted sources. <br>
Risk: Voice cloning can reproduce a speaker's voice and may create consent or misuse concerns. <br>
Mitigation: Clone voices only with explicit permission and keep consent records aligned with the deployment's policy. <br>
Risk: Uploaded voice profiles may persist in local speaker cache files. <br>
Mitigation: Review and delete cached speaker files when voice profiles should not remain on disk. <br>


## Reference(s): <br>
- [Fish Audio S2 Pro model card](https://huggingface.co/fishaudio/s2-pro) <br>
- [S2 Pro technical report](https://arxiv.org/abs/2603.08823) <br>
- [API Reference](references/api-reference.md) <br>
- [Architecture](references/architecture.md) <br>
- [Emotion & Style Tags](references/emotion-tags.md) <br>
- [LoRA Fine-tuning](references/finetune.md) <br>
- [Installation Guide](references/install.md) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/fish-speech) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, cURL examples, request parameters, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for local servers, containers, OpenAI-compatible API calls, voice cloning, streaming, batch synthesis, and fine-tuning workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
