## Description:

Generates reusable multi-step agent workflow blueprints for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to define ordered agent workflow blueprints with triggers, step contracts, dependencies, and fallback behavior for handoff to tools such as n8n or internal orchestrators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper generator can write or overwrite files even when dry-run mode is requested.

Mitigation: Review or fix the generator before production use, do not rely on --dry-run as safe, and only invoke it with output paths confined to a disposable or intended artifact directory.

Risk: Workflow steps that transmit data externally can create exfiltration risk if destination endpoints and fields are not explicit.

Mitigation: Confirm the destination endpoint and the specific data fields before generating any workflow step that transmits data externally.

Risk: Generated workflows may include destructive operations such as delete, drop, overwrite, or force-push.

Mitigation: Include an explicit human confirmation gate as a separate workflow step before any destructive operation.

Risk: Workflow steps that fetch and execute remote scripts can bypass code review and introduce supply-chain risk.

Mitigation: Reference only local project scripts under ./scripts/ in workflow steps and vendor external code locally before use.

## Reference(s):

- [Workflow Blueprint Guide](artifact/references/workflow-blueprint-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/agentic-workflow-automation-hardened)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/agentic-workflow-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and exportable JSON, Markdown, or CSV workflow blueprint artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled generator normalizes workflow steps and can export artifacts; input JSON is capped at 1 MiB.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
