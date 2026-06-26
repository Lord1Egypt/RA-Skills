## Description: <br>
Ai Resource Master estimates GPU and server capacity for medical large-model scenarios from outpatient and inpatient volumes and selected AI use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellohushuai](https://clawhub.ai/user/hellohushuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare planners, solution architects, and technical teams use this skill to collect patient volume and scenario inputs, calculate daily LLM workload, and produce a capacity estimate for GPU cards and appliance counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capacity estimates can be misleading if the target GPU model, concurrency, utilization, coverage rates, or appliance sizing differs from the skill defaults. <br>
Mitigation: Confirm the assumptions against the deployment environment and adjust the inputs or hardware parameters before relying on the estimate. <br>
Risk: The skill produces calculation guidance only and does not validate clinical appropriateness, procurement constraints, or compliance requirements. <br>
Mitigation: Review outputs with healthcare operations, infrastructure, and compliance stakeholders before using them for planning decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hellohushuai/ai-resource-master) <br>
- [Calculation Parameters](references/calculation-params.md) <br>
- [Example Output](references/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style capacity assessment report with plain text sections and calculations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outpatient volume, inpatient volume, and selected AI scenarios; uses default coverage rates and 910B3/Huawei appliance assumptions when users do not provide alternatives.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact _meta.json lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
