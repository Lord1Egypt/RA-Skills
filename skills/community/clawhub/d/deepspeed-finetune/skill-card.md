## Description: <br>
Fine-tune large language models using DeepSpeed on local or remote GPUs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delock](https://clawhub.ai/user/delock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to plan and run DeepSpeed fine-tuning workflows for large language models on local or remote GPU systems, including LoRA/QLoRA, ZeRO configuration, launch commands, monitoring, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad SSH-level control of remote training machines. <br>
Mitigation: Use a non-root remote account, review remote commands before execution, and run training in an isolated environment. <br>
Risk: Persistent SSH keys or passwordless access can remain usable after setup. <br>
Mitigation: Avoid no-passphrase keys unless revocation is understood, scope credentials to the training host, and remove keys or sessions when training is complete. <br>
Risk: Host key verification gaps can expose remote training sessions to connection spoofing. <br>
Mitigation: Verify host keys before routine use and add trusted host keys to known_hosts for subsequent connections. <br>
Risk: Untrusted models or datasets can introduce unsafe code or data handling behavior during fine-tuning. <br>
Mitigation: Run untrusted inputs in an isolated environment and explicitly review model loading options, especially remote-code settings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/delock/deepspeed-finetune) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/delock) <br>
- [Metadata Homepage](https://github.com/deepspeedai/deepspeed-skills/tree/main/openclaw/deepspeed-finetune) <br>
- [Quick Start Guide](references/quick_start.md) <br>
- [DeepSpeed Reference Guide](references/deepspeed_guide.md) <br>
- [LoRA/QLoRA Fine-tuning Guide](references/lora_guide.md) <br>
- [ZeRO Optimization Guide](references/zero_optimization.md) <br>
- [Single-GPU Training Strategy](references/single_gpu_strategy.md) <br>
- [Remote Training Guide](references/remote_training.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [DeepSpeed Documentation](https://www.deepspeed.ai/) <br>
- [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed) <br>
- [ZeRO Paper](https://arxiv.org/abs/1910.02054) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, JSON configuration examples, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce executable training and SSH commands that require review before running.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
