## Description:

Fine-tune large language models using DeepSpeed on local or remote GPUs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delock](https://clawhub.ai/user/delock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to plan and run LLM fine-tuning with DeepSpeed, LoRA or QLoRA, ZeRO optimization, local or remote GPU execution, and training monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote SSH control can create lasting passwordless access to a training machine.

Mitigation: Use a dedicated unprivileged remote account and remove any generated key from both the local machine and the remote authorized_keys file when finished.

Risk: Password-based SSH and unsafe host-key handling can expose remote training connections to credential or man-in-the-middle risk.

Mitigation: Avoid password-based SSH where possible and verify host keys out of band before relying on the remote connection.

Risk: Enabling trust_remote_code for an unreviewed model can execute model-provided code.

Mitigation: Do not enable trust_remote_code unless the model source and code have been reviewed and trusted.

## Reference(s):

- [Quick Start Guide](references/quick_start.md)
- [DeepSpeed Guide](references/deepspeed_guide.md)
- [LoRA/QLoRA Fine-tuning Guide](references/lora_guide.md)
- [ZeRO Optimization Guide](references/zero_optimization.md)
- [Single-GPU Training Strategy](references/single_gpu_strategy.md)
- [Remote Training Guide](references/remote_training.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/delock/skills/deepspeed-finetune)
- [Metadata Homepage](https://github.com/deepspeedai/deepspeed-skills/tree/main/openclaw/deepspeed-finetune)
- [DeepSpeed Documentation](https://www.deepspeed.ai/)
- [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed)
- [ZeRO Paper](https://arxiv.org/abs/1910.02054)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local training commands, remote training commands, DeepSpeed configuration files, and monitoring guidance.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
