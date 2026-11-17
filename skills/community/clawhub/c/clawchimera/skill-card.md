## Description:

Runs VPS performance and network tests covering system information, CPU, memory, disk, streaming access, IP quality, mail ports, routing, latency, and speed checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiritlhls](https://clawhub.ai/user/spiritlhls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to benchmark VPS instances and generate AI-ready analysis prompts from benchmark output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an upstream native binary at runtime.

Mitigation: Run it in a constrained non-root environment and require pinned, verified downloads before treating it as routine-risk.

Risk: Benchmark reports can expose public IP, provider, route, port, and system fingerprints.

Mitigation: Treat generated reports as sensitive and review them before sharing or pasting into external systems.

Risk: Result upload is enabled by default in the exposed arguments.

Mitigation: Pass -upload=false unless public sharing is intentional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spiritlhls/skills/clawchimera)
- [ClawChimera Homepage](https://github.com/oneclickvirt/ClawChimera)
- [Upstream ECS Project](https://github.com/oneclickvirt/ecs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown, including shell command examples and AI analysis prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create goecs.txt in the working directory and may upload benchmark results when upload remains enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
