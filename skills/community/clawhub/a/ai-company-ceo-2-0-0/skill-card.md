## Description:

AI Company CEO helps an agent design and operate an all-AI company using a hub-and-spoke organization model, orchestrator-worker collaboration, guardrails, prompt CI/CD, KPI tracking, and NIST AI RMF alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for CEO-style governance, operating-model, KPI, prompt-release, and cross-agent coordination guidance for an all-AI company. It produces structured decisions, action plans, stakeholder lists, and risk-aware operating procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file, network, and cross-agent authority.

Mitigation: Run it only in a tightly sandboxed workspace with restricted file paths and approved API destinations.

Risk: Delegation across agents can expose sensitive business, legal, financial, HR, or security context.

Mitigation: Require explicit approval before sending sensitive context to other agents or external services.

Risk: Mutable or unpinned dependencies can change behavior after installation.

Mitigation: Pin dependency versions and review changes before deployment.

Risk: The artifact can produce executive guidance that affects operations and governance decisions.

Mitigation: Review generated decisions and action plans before operational use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/johnsmithfan/skills/ai-company-ceo-2-0-0)
- [ClawHub homepage metadata](https://clawhub.com/skills/ai-company-ceo)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown decision reports with tables, action plans, KPI summaries, stakeholder lists, and audit markers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-shaped decision, action_plan, kpis, and stakeholders fields described by the skill interface.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
