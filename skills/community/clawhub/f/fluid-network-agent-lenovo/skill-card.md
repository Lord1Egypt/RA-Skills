## Description:

Reads steady-state incompressible fluid networks from TOML, solves node pressures and pipe flow, and reports scenario-level connectivity and load reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zebra6-web](https://clawhub.ai/user/zebra6-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a TOML description of a fluid network into scenario reports comparing pressures, flows, connectivity, and PASS/FAIL reliability against load thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local script reads TOML input and can write a report to an optional output path.

Mitigation: Review TOML files the agent drafts or edits, and choose the output path deliberately before execution.

Risk: Scenario PASS/FAIL results depend on simplified steady-state incompressible assumptions and user-provided thresholds.

Mitigation: Use the report as an engineering aid and verify model assumptions, units, and thresholds before relying on results.

## Reference(s):

- [Fluid Network Agent on ClawHub](https://clawhub.ai/zebra6-web/skills/fluid-network-agent-lenovo)
- [TOML Schema Reference](artifact/reference.md)
- [Examples](artifact/examples.md)
- [Example Network TOML](artifact/examples/example_network.toml)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON scenario reports with inline values for connectivity, edge results, and function reliability.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated report to a user-selected output path when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
