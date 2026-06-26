## Description: <br>
Checks export scope, destination, privacy, redaction, and approval before files, records, datasets, logs, or account data are exported or shared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to review proposed data exports before sharing files, records, datasets, logs, reports, messages, or account data. It helps decide whether to proceed, narrow scope, ask for more detail, redact, request approval, route to review, or block the export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the skill as an enforcement mechanism even though the security evidence identifies it as advisory instruction text. <br>
Mitigation: Confirm operational users understand that it provides guardrail guidance and pair it with actual access controls, approval workflows, or review tooling where enforcement is required. <br>
Risk: Marketplace capability tags include broad labels that may affect policy routing or trust decisions. <br>
Mitigation: Review the published capability tags before relying on them for automated policy, trust, or routing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-data-export-guardrail-skill) <br>
- [Data export guardrail schema](artifact/schemas/data-export-guardrail.schema.json) <br>
- [Redacted data export guardrail example](artifact/examples/redacted-data-export-guardrail.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with a structured text decision pattern] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no code execution, package installation, persistence, service calls, or data export is performed by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
