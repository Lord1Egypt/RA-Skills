## Description:

The stateful control router for FDE Delivery Loop identifies the current stage of a customer engagement, selects the most appropriate FDE specialist skill, preserves gates, artifacts, versions, owners, decisions, and rollback history, and identifies one next material action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

Delivery teams, forward-deployed engineers, and agents use this skill to classify customer-engagement evidence, route work to the earliest appropriate FDE delivery stage, and maintain concise project state for continuations, handoffs, audits, and failure reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write local project status and event-history files that may include delivery decisions and references to customer work.

Mitigation: Store state files inside the intended project workspace and avoid secrets, personal data, restricted content, or full customer source material in fde-project.json or fde-events.jsonl.

Risk: The event log records append-only delivery history but is not compliance-grade tamper-proof audit evidence by itself.

Mitigation: Use stronger external controls when regulated audit integrity is required, and treat the skill's event log as operational project memory.

Risk: Routing output can recommend stage advancement, skipped gates, or owner changes that affect delivery decisions.

Mitigation: Require human confirmation before advancing stages, skipping quality gates, or changing responsible owners and key decisions.

## Reference(s):

- [Engagement State Machine](references/engagement-state-machine.md)
- [FDE Operating Model](references/fde-operating-model.md)
- [Input Examples](references/input-examples.md)
- [Project State Contract](references/project-state-contract.md)
- [Public Method Sources](references/public-sources.md)
- [Router Field Handbook](references/router-field-handbook.md)
- [Router Quality Rubric](references/router-quality-rubric.md)
- [Routing Contract](references/routing-contract.md)
- [GOV.UK: How the Discovery Phase Works](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works)
- [AWS: Generative AI Lifecycle Operational Excellence Framework](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/understanding-gloe.html)
- [AWS: Advancing from POC to Pre-production](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-advancing.html)
- [Microsoft Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/overview)
- [OpenAI Forward Deployed Engineer Job Description](https://openai.com/careers/forward-deployed-engineer-%28fde%29-nyc-new-york-city/)
- [Stripe Forward Deployed Engineering](https://stripe.com/jobs/listing/backend-engineer-forward-deployed-engineering/7249744)
- [Palantir UK Careers](https://www.palantir.com/uk/careers/)
- [Forward Deployed Engineer Roadmap](https://github.com/thecoder8890/forward-deployed-engineer-roadmap)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with routing summaries, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local fde-project.json and fde-events.jsonl state files when used for stateful delivery.]

## Skill Version(s):

1.0.0 (source: server release evidence and TRUST-CARD.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
