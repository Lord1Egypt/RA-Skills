## Description: <br>
Generate reusable multi-step agent workflow blueprints for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to define ordered trigger/action workflows with explicit dependencies, fallback behavior, and implementation handoff artifacts for platforms such as n8n or internal orchestrators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow steps that transmit data externally can expose unspecified or sensitive fields. <br>
Mitigation: Confirm the destination endpoint and exact data fields before generating any external transmission step. <br>
Risk: Destructive operations such as delete, drop, overwrite, or force-push can cause irreversible changes. <br>
Mitigation: Include a separate human confirmation gate before any destructive workflow step. <br>
Risk: Dynamic download-and-execute patterns or remote scripts can bypass code review and introduce supply chain risk. <br>
Mitigation: Reference only reviewed local project scripts from ./scripts/ in generated workflow steps. <br>
Risk: The local generator writes to the output path even when dry-run is set. <br>
Mitigation: Avoid pointing --output at sensitive or existing files unless overwriting them is intended. <br>


## Reference(s): <br>
- [Workflow Blueprint Guide](references/workflow-blueprint-guide.md) <br>
- [Safety Evaluation](SAFETY.md) <br>
- [Faberlens Guardrail Evidence](https://faberlens.ai/explore/agentic-workflow-automation) <br>
- [ClawHub Release Page](https://clawhub.ai/snazar-faberlens/agentic-workflow-automation-hardened) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated JSON, Markdown, or CSV workflow blueprint files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled local generator writes artifacts to the requested output path; do not rely on dry-run to suppress writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
