## Description:

Autoresearch helps agents run autonomous neural network experiments by modifying training code, launching fixed-budget runs, evaluating validation bits per byte, and logging results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyunrei2025](https://clawhub.ai/user/baiyunrei2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML researchers use this skill to set up single-GPU autonomous experiments where an agent modifies train.py, runs five-minute training trials, evaluates val_bpb, and records results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous experiments can continue editing and running GPU training code, consuming compute and cost.

Mitigation: Run only in a disposable sandbox with explicit maximum run count, time, and cost limits.

Risk: Setup and runtime dependency paths can introduce supply-chain exposure.

Mitigation: Avoid curl|sh setup, pin and lock dependencies and kernels, and review dependencies before use.

Risk: Autonomous git reset or commit batches can discard useful work.

Mitigation: Use a dedicated branch and require approval before git reset or commit batches.

Risk: Running in a normal workspace can expose credentials or sensitive files.

Mitigation: Do not run the skill in an environment containing valuable credentials or sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiyunrei2025/skills/autoresearch-karpathy)
- [Autoresearch source project](https://github.com/karpathy/autoresearch)
- [Nanochat implementation](https://github.com/karpathy/nanochat)
- [uv documentation](https://docs.astral.sh/uv/)
- [Climbmix dataset shards](https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle/resolve/main)
- [Project announcement](https://x.com/karpathy/status/2029701092347630069)
- [Dummy's Guide](https://x.com/hooeem/status/2030720614752039185)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, Python code edits, and tab-separated experiment logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Experiments report val_bpb, training time, total time, peak VRAM, MFU, total tokens, step count, parameter count, depth, and keep/discard/crash status.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
