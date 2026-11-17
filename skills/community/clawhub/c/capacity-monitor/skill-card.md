## Description:

Monitors system resource utilization and reports idle capacity for workload scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and workload schedulers use this skill to inspect local CPU and memory availability, identify idle capacity, and support resource optimization, capacity planning, or load-balancing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reports local CPU and memory availability, which can expose basic host utilization to the invoking agent or scheduler.

Mitigation: Run it only where sharing basic local resource metrics with that agent or scheduler is acceptable.

Risk: The documentation is Chinese-only, which can make behavior and output expectations easier to misunderstand for some operators.

Mitigation: Have operators review or translate the usage notes and JSON output format before deployment in non-Chinese-language environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ink5725/skills/capacity-monitor)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [JSON capacity report and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a timestamp, CPU idle percentage, available memory in MB, and completion status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
