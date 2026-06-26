## Description: <br>
Stop agents from "forgetting, mixing projects, and rotting over time" by giving them a practical memory operating system: global memory, project memory, promotion rules, validation cases, and a maintenance loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aslan-ai-labs](https://clawhub.ai/user/aslan-ai-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design long-term memory for AI agents, separate global and project-specific knowledge, promote reusable lessons, validate recovery and reuse, and maintain the memory system over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or personal information could be promoted into shared or global memory if users apply the workflow without privacy boundaries. <br>
Mitigation: Define allowed memory content before broad use, avoid secrets and personal identifiers, and apply the skill's privacy-preserving abstraction guidance before publishing or sharing outputs. <br>
Risk: Stale or project-specific details could become durable rules and affect unrelated future work. <br>
Mitigation: Use evidence-based promotion, scope and boundary fields, validation cases, and periodic reviews to deprecate outdated or overly local rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aslan-ai-labs/agent-memory-os) <br>
- [Architecture Decision Guide](references/architecture-decision-guide.md) <br>
- [Architecture](references/architecture.md) <br>
- [Failure Modes](references/failure-modes.md) <br>
- [Routing](references/routing.md) <br>
- [Promotion](references/promotion.md) <br>
- [Validation](references/validation.md) <br>
- [Maintenance](references/maintenance.md) <br>
- [Publish Checklist](references/publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with reusable templates and structured runbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only skill; no tools, API keys, or runtime integrations detected.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
