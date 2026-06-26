## Description: <br>
Autonomously validates specifications, runs behavioral tests, generates code, executes tests, and produces outcome reports with integrity metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate structured specifications, run mock behavioral tests, orchestrate code generation checkpoints, and produce JSON outcome reports for review or feedback-loop analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill presents simulated results and a simple hash as verified signed proof. <br>
Mitigation: Treat pass rates, security evidence, and signature fields as local mock outputs only; require independent testing and trusted signing before release, compliance, or production use. <br>
Risk: The release is tagged as requiring wallet access, but the security guidance says wallet access should not be granted without clearer scoping. <br>
Mitigation: Run without wallet access unless a future version documents why wallet permissions are needed and how they are constrained. <br>


## Reference(s): <br>
- [Dark Factory Skill Page](https://clawhub.ai/danielfoojunwei/dark-factory) <br>
- [Specification Schema](artifact/references/specification_schema.json) <br>
- [Outcome Report Schema](artifact/references/outcome_report_schema.json) <br>
- [Behavioral Testing Guide](artifact/references/behavioral_testing_guide.md) <br>
- [Dark Factory Operations](artifact/references/dark_factory_operations.md) <br>
- [Triad Integration](artifact/references/triad_integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON outcome reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates specification validation results, behavioral test reports, placeholder implementation files, and outcome_report JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
