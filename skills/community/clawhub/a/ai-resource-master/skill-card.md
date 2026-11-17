## Description:

Ai Resource Master helps agents estimate healthcare AI server and GPU capacity needs from outpatient volume, inpatient volume, selected healthcare AI scenarios, coverage assumptions, and GPU capacity defaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellohushuai](https://clawhub.ai/user/hellohushuai)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare planners, solution architects, and implementation teams use this skill to collect annual outpatient and inpatient volumes, choose healthcare AI application scenarios, and generate a concise resource-sizing report for GPU cards, appliance count, and optional total compute.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default sizing assumptions may not match a specific deployment, especially 910B3 GPU capacity, Huawei appliance sizing, coverage rates, and per-scenario timing.

Mitigation: Review and adjust the built-in defaults against local workload data, target hardware, service-level expectations, and procurement requirements before relying on outputs.

Risk: Healthcare resource-sizing prompts can become sensitive if users provide patient-identifiable or overly granular operational data.

Mitigation: Provide aggregate outpatient and inpatient volumes and avoid patient-identifiable data when using the skill.

## Reference(s):

- [Calculation Parameters](references/calculation-params.md)
- [Example Output](references/example-output.md)
- [ClawHub Skill Page](https://clawhub.ai/hellohushuai/skills/ai-resource-master)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown-style prose report with scenario-by-scenario calculations and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language healthcare AI resource-sizing reports using built-in scenario timing, coverage-rate, 910B3 GPU, and Huawei appliance assumptions unless the user supplies alternatives.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
