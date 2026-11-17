## Description:

Fish Audio S2 Pro TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and call Fish Audio S2 Pro text-to-speech services, including OpenAI-compatible API use, streaming, voice cloning, emotion tags, multi-speaker synthesis, and Slow AR LoRA fine-tuning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposed TTS or voice-cloning services may be reachable beyond the intended host.

Mitigation: Prefer loopback-only binding or explicit network controls before enabling service endpoints.

Risk: Mutable package, model, or container installs can change behavior between deployments.

Mitigation: Pin package versions, model revisions, and container digests before production use.

Risk: Voice cloning can misuse speaker identity or retain sensitive biometric samples.

Mitigation: Use voice cloning only with explicit speaker permission and confirm retention and deletion behavior for uploaded voice samples.

Risk: Reference audio accepted from arbitrary URLs or file paths can expand data exposure and operational risk.

Mitigation: Avoid arbitrary URL and file:// reference audio unless sources are trusted and access is scoped.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/fish-speech)
- [Fish Audio S2 Pro Model](https://huggingface.co/fishaudio/s2-pro)
- [Fish Audio S2 Pro Technical Report](https://arxiv.org/abs/2603.08823)
- [Installation Guide](references/install.md)
- [API Reference](references/api-reference.md)
- [S2 Pro Architecture](references/architecture.md)
- [Emotion & Style Tags](references/emotion-tags.md)
- [LoRA Fine-tuning](references/finetune.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, API request examples, Python snippets, parameter tables, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance for TTS deployment, voice cloning, streaming audio, model downloads, and fine-tuning workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
