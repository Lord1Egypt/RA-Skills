## Description:

Stage 4 of FDE Delivery Loop. Turn an approved POC PRD into a runnable, risk-controlled deployment architecture and delivery plan covering system boundaries, data, permissions, integrations, environments, observability, and risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, field delivery engineers, architects, and technical owners use this skill to turn an approved POC PRD into a deployment architecture and risk package for controlled POC implementation planning, architecture review, data and permission mapping, integration design, and pre-deployment risk decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive customer system details, data classifications, IAM information, logs, or production-readiness context while planning.

Mitigation: Provide only information appropriate for the planning context, minimize sensitive fields, and route real production changes through normal approval and security review.

Risk: A runnable POC design could be mistaken for production approval.

Mitigation: Keep POC and production boundaries explicit, document technical debt and production gaps, and require security, compliance, and owner approval before production connection, external data transfer, permission changes, deployment, or rollback.

Risk: Architecture proposals may contain incorrect assumptions about integrations, permissions, or customer environments.

Mitigation: Mark missing interface, access, data, or acceptance evidence as assumptions and validate through documentation, customer owner confirmation, environment checks, or real testing before implementation.

## Reference(s):

- [Deployment Architecture and Risk Package Template](references/deployment-architecture-pack.md)
- [Deployment Architecture Input Guide](references/architecture-input-guide.md)
- [POC Deployment Architecture Rules](references/architecture-rules.md)
- [Agent Deployment Security Check](references/security-checklist.md)
- [POC Technology Selection Guide](references/technology-selection-guide.md)
- [Deployment Architecture Quality Score](references/architecture-quality-rubric.md)
- [POC Architecture Field Manual](references/architecture-field-handbook.md)
- [Complete Example of Deployment Architecture](references/architecture-worked-example.md)
- [POC to Production Transition](references/production-transition.md)
- [Public Method Sources](references/public-sources.md)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [Microsoft: Architects Collaborate With Workload Teams](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/collaboration)
- [Martin Fowler: Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-riREDACTED-SECRET)
- [OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [Azure: Architecture Testing Strategy](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown architecture and risk package with tables, decision records, checklists, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning and review documents only; it does not change cloud resources, networks, IAM, or production systems by default.]

## Skill Version(s):

1.0.0 (source: server release metadata and TRUST-CARD.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
