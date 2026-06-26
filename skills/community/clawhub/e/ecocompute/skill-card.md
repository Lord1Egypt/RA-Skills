## Description: <br>
EcoCompute gives evidence-first, stateless advice for optimizing LLM inference energy use with measured benchmark priors and anti-pattern checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongping-zh](https://clawhub.ai/user/hongping-zh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use EcoCompute to compare LLM inference configurations, audit wasted energy, and receive conservative GPU, model, precision, and batching recommendations grounded in benchmark data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark recommendations may not transfer to newer software stacks, unmeasured hardware, non-NVIDIA systems, or multi-GPU deployments. <br>
Mitigation: Treat recommendations as advisory, verify against local measurements before changing production inference settings, and preserve the skill's confidence downgrades and boundary notes. <br>
Risk: Incomplete user inputs can make numeric energy guidance less precise. <br>
Mitigation: Ask for GPU, model, precision, batch size, latency target, and cost constraints when available; otherwise label assumptions and extrapolations clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongping-zh/ecocompute) <br>
- [Benchmark dataset archive](https://zenodo.org/records/18900289) <br>
- [Quantization energy crossover dataset](https://github.com/ecocompute-ai/quantization-energy-crossover) <br>
- [Live EcoCompute dashboard](https://hongping-zh.github.io/) <br>
- [Reference implementation](https://github.com/hongping-zh/ecocompute-dynamic-eval) <br>
- [MLCommons Power Working Group issue](https://github.com/mlcommons/inference/issues/2558) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with tables, confidence labels, benchmark citations, and inline configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only advisory output; no host actions, persistence, credentials, or automated benchmark execution.] <br>

## Skill Version(s): <br>
3.0.8 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
