## Description:

EcoCompute is a prompt-only advisory skill that gives evidence-first recommendations for improving LLM inference energy efficiency using measured benchmark priors and anti-pattern detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongping-zh](https://clawhub.ai/user/hongping-zh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to compare LLM inference precision, GPU, batching, and serving choices against benchmark-backed energy guidance. It helps audit inefficient configurations, explain energy overhead, and produce framework-specific configuration suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark numbers may not match a user's production stack, newer framework versions, or hardware outside the measured set.

Mitigation: Treat recommendations as guidance tied to the stated 2025-Q1 dataset and verify them against the user's own hardware, framework versions, and production requirements.

Risk: Users may over-apply quantization advice where the artifact says coverage is extrapolated or out of scope.

Mitigation: Use the skill's confidence labels and boundary notes for unsupported GPUs, newer stacks, multi-GPU deployments, and models beyond the measured range.

Risk: The skill is advisory and cannot observe the user's machine or validate live runtime behavior.

Mitigation: Use it as a decision aid, then confirm changes with local measurement before making operational changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongping-zh/skills/ecocompute)
- [Zenodo benchmark dataset 18900289](https://zenodo.org/records/18900289)
- [Quantization energy crossover dataset repository](https://github.com/ecocompute-ai/quantization-energy-crossover)
- [EcoCompute live dashboard](https://hongping-zh.github.io/)
- [Reference implementation](https://github.com/hongping-zh/ecocompute-dynamic-eval)
- [MLCommons Inference issue 2558](https://github.com/mlcommons/inference/issues/2558)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, confidence labels, inline code snippets, and brief shell commands when installation is discussed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only advisory output; it does not create files, install dependencies, execute code, or access the user's host environment.]

## Skill Version(s):

3.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
