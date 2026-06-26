## Description: <br>
Generate reusable multi-step agent workflow blueprints for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to define workflow names, triggers, ordered steps, fallback behavior, and portable blueprint artifacts for automation platforms or internal orchestrators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dry-run option still writes an output file, so users may overwrite an existing artifact unintentionally. <br>
Mitigation: Choose output paths deliberately and review generated files before using them in an automation workflow. <br>
Risk: Workflow inputs can be copied into generated artifacts, including sensitive values if users provide them. <br>
Mitigation: Avoid putting secrets or private credentials in workflow inputs and scan artifacts before sharing or deployment. <br>


## Reference(s): <br>
- [Workflow Blueprint Guide](references/workflow-blueprint-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance and generated workflow blueprint files in JSON, Markdown, or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts include workflow name, trigger metadata, ordered steps, fallback behavior, and an n8n-style blueprint structure.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
