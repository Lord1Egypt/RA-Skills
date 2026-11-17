## Description:

GHL Lead Qualifier automates GoHighLevel lead triage over WhatsApp/SMS, extracting budget, urgency, and needs to support CRM tagging and Kanban stage updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

External sales and operations teams use this skill to triage inbound GoHighLevel leads over WhatsApp/SMS, classify intent and urgency, and prepare CRM tag or Kanban stage updates. It is intended for lead qualification workflows that already have consent, credential scoping, and human approval controls for outreach and record changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact leads and change CRM records, which could create unwanted outreach or incorrect opportunity updates.

Mitigation: Use human approval rules for outbound messages and CRM stage changes, and confirm WhatsApp/SMS consent before use.

Risk: The skill depends on CRM and gateway credentials that could grant broad account access.

Mitigation: Use GoHighLevel and Habilis tokens scoped to the minimum permissions needed and rotate them according to local policy.

Risk: The artifact references an unbundled local CRM client path, making behavior harder to review before deployment.

Mitigation: Use a reviewed or bundled CRM client and treat the external local path as unsupported until separately authorized.

Risk: The artifact includes support, finance, PAPI, and operational-routing sections beyond the core lead qualification workflow.

Mitigation: Treat those sections as out of scope unless the deploying team has separate authorization, controls, and review for those workflows.

## Reference(s):

- [Padrões de Triagem e Classificação de Leads no GHL](references/unanswered_leads_triaging_patterns.md)
- [Habilis MCP Gateway developer portal](https://ia.sthub.com.br)
- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/ghl-lead-qualifier)
- [ClawHub publisher profile](https://clawhub.ai/user/rafacpti23)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose outbound WhatsApp/SMS responses, lead classifications, CRM tags, and CRM stage-change commands for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
