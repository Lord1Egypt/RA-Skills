## Description: <br>
Tune AITER's CK GEMM and fused MoE kernels for specific model shapes on AMD GPUs, covering shape discovery from inference logs, baseline benchmarking, kernel tuning, and before/after performance comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexsun07](https://clawhub.ai/user/alexsun07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to tune AITER CK GEMM and fused MoE kernels for specific model shapes on AMD GPU systems, then compare before and after benchmark results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can run remote shell commands, edit tuning-related AITER files, and launch long GPU tuning jobs. <br>
Mitigation: Use it only on an approved, trusted AITER/ROCm host or container; confirm the target environment, file paths, log destinations, and background jobs before execution, and monitor GPU usage until tuning completes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alexsun07/aiter-ck-gemm-tune) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [parse_untuned_shapes.py](artifact/scripts/parse_untuned_shapes.py) <br>
- [compare_results.py](artifact/scripts/compare_results.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, CSV configuration paths, and benchmark comparison output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify untuned/tuned CSV files, tuning logs, benchmark logs, and tuning reports in the target AITER environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
