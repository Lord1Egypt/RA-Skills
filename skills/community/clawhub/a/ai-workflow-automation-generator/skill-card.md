## Description:

Generates a custom AI automation playbook identifying workflows to automate, recommended tools, SOPs, and ROI projections for small businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitflopez](https://clawhub.ai/user/gitflopez)

### License/Terms of Use:

MIT-0

## Use Case:

Small business owners, operations managers, consultants, and solopreneurs use this skill to turn business workflow details into an AI automation audit, tool stack recommendation, AI-integrated SOP, and 90-day implementation roadmap with ROI projections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share sensitive business process details with an AI assistant while completing the prompt templates.

Mitigation: Remove confidential customer, employee, financial, and credential data before submitting workflow details to an AI assistant.

Risk: Suggested tools, pricing, API use, or compliance assumptions may be inaccurate or unsuitable for a specific business.

Mitigation: Independently verify tool capabilities, current pricing, API terms, integration requirements, and compliance obligations before implementation.

Risk: Customer-facing or sensitive workflows may produce poor outcomes if automated without review.

Mitigation: Keep the human checkpoints, error handling, and fallback manual process described by the SOP prompt for high-impact workflow steps.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/gitflopez/skills/ai-workflow-automation-generator)
- [Artifact README](artifact/README.md)
- [Workflow Audit Prompt](artifact/prompts/01-workflow-audit.md)
- [AI Tool Stack Recommendation Prompt](artifact/prompts/02-tool-stack.md)
- [SOP with AI Integration Prompt](artifact/prompts/03-sop-ai-integration.md)
- [Implementation Roadmap and ROI Projection Prompt](artifact/prompts/04-implementation-roadmap.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown prompt templates and structured business automation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided business workflow, budget, tool stack, SOP, labor-cost, and implementation-constraint details.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
