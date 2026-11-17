## Description:

Generates Python runner scripts and JSON scenario files for AgentScope benchmarking workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers generate latency, throughput, and prompt-comparison benchmark scaffolds for AgentScope workflows. They must connect the generated placeholder runners to real agent calls before relying on the measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files may replace similarly named files in the chosen output directory.

Mitigation: Generate into a dedicated benchmark directory and review its contents before running the scripts.

Risk: Benchmark results may include prompt text when adapted for real agent calls.

Mitigation: Review results and remove sensitive prompt content before sharing.

## Reference(s):

- [AgentScope project (skill homepage)](https://github.com/agentscope-ai/agentscope)
- [ClawHub skill listing](https://clawhub.ai/trend0522/skills/agentscope-benchmark-runner)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands]

**Output Format:** [Python scripts and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates latency, throughput, and comparison scenarios; generated runners contain placeholder agent calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
