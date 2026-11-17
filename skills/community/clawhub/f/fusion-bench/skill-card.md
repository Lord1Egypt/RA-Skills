## Description:

Use FusionBench to run model fusion experiments, including benchmarks, new merging algorithms, fused model evaluation, and model pool management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanganke](https://clawhub.ai/user/tanganke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate FusionBench for model merging experiments, benchmark runs, method comparisons, and custom model fusion algorithm development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to install an unpinned Python package and run model benchmark commands.

Mitigation: Install FusionBench in a virtual environment or container, avoid administrator privileges for package installs, and pin or verify package versions when reproducibility or supply-chain control matters.

Risk: Benchmark and model fusion workflows may download or cache model artifacts and can require meaningful compute resources.

Mitigation: Review storage, network, and compute requirements before execution, and use isolated cache locations when running shared or sensitive workloads.

## Reference(s):

- [FusionBench repository](https://code.tanganke.com/tanganke/fusion_bench)
- [FusionBench documentation](https://tanganke.github.io/fusion_bench/)
- [FusionBench paper](https://arxiv.org/abs/2406.03280)
- [ClawHub skill page](https://clawhub.ai/tanganke/skills/fusion-bench)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, Python snippets, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
