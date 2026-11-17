## Description:

Provides AC branch pi-model power-flow equations and Python helpers for P/Q and apparent-power calculations with transformer tap ratio and phase shift using MATPOWER branch fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power-systems engineers use this skill to compute AC branch flows in both directions, evaluate MVA limits and branch loading, aggregate branch contributions for nodal balance, and debug sign or unit issues in AC optimal power flow work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect formula application or domain assumptions could produce misleading power-flow results.

Mitigation: Review the equations and computed outputs against the target network model and operational conventions before using results for decisions.

Risk: Example code reads network data from a file path supplied by the user or agent workflow.

Mitigation: Only point the helper code at network data files that are intended for the agent to read.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/energy-ac-optimal-power-flow-ac-branch-pi-model)
- [Publisher profile](https://clawhub.ai/user/wu-uk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python code examples and equations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-unit P/Q branch-flow values and guidance for converting apparent power to MVA with baseMVA.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
