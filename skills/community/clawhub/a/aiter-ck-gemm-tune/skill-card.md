## Description:

Tune AITER's CK GEMM and fused MoE kernels for specific model shapes on AMD GPUs, including shape discovery from inference logs, baseline benchmarking, kernel tuning, and before/after performance comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexsun07](https://clawhub.ai/user/alexsun07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to tune AMD AITER CK GEMM and fused MoE kernels for model-specific inference shapes, then compare before and after benchmark results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify files in an installed AITER checkout while preparing tuning inputs or adapting benchmark scripts.

Mitigation: Run it in a controlled container or disposable branch, and confirm the files to be changed before allowing edits.

Risk: The tuning workflow may launch persistent multi-GPU background jobs.

Mitigation: Avoid detached nohup jobs unless they are intended, record the launched process and log paths, and keep a clear stop procedure.

Risk: Tuning on shared GPU nodes can consume hardware for long periods.

Mitigation: Check GPU availability first, set explicit parallelism and timeout options, and coordinate usage with other users of the node.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python helper scripts, CSV tuning inputs, benchmark logs, and comparison reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMD GPU environment with AITER installed; tuning runs can be long-lived and hardware-dependent.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
