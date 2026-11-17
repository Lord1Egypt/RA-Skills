## Description:

Connects AI agents to GoHighLevel API v2 workflows for contact management, Kanban opportunity updates, unanswered lead triage, workflow triggers, direct messaging, and real-time webhook lead ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to configure and guide CRM automations that create or update contacts, move opportunities through GoHighLevel pipelines, triage unanswered leads, send direct messages, and receive webhook lead events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle live GoHighLevel and Meta credentials with broad CRM account access.

Mitigation: Do not paste tokens into chat; store credentials in a local environment file or secret manager and use least-privilege private integration scopes.

Risk: Sensitive CRM operations may be routed through an unreviewed third-party gateway or local components.

Mitigation: Use the third-party gateway or local scripts only after auditing the source, permissions, token handling, and operational trust boundaries.

Risk: Webhook-driven lead handling can trigger actions across tenants or accounts if endpoints are unauthenticated or misrouted.

Mitigation: Use HTTPS webhooks that are authenticated, signed, tenant-bound, and logged before handling real leads or triggering CRM actions.

Risk: CRM automation can modify contacts, opportunities, messages, workflows, or other business records.

Mitigation: Require explicit human approval for destructive or bulk-changing actions and review generated commands before execution.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/rafacpti23/skills/ghl-integration)
- [Habilis developer portal](https://xvix.com.br)
- [GoHighLevel API v2 Integration Insights](artifact/references/ghl_api_v2_insights.md)
- [Instagram Follow-Gate & GoHighLevel Sync Pattern](artifact/references/instagram_follow_gate_ghl_sync.md)
- [GHL API v2 Custom Provider and Contact Resolution Reference](artifact/references/stevo-whatsapp.md)
- [GHL Unanswered Leads Triaging & Pattern Recognition](artifact/references/unanswered_leads_triaging_patterns.md)
- [Zero-Touch Orchestration & Dynamic Webhook Architecture](artifact/references/zero_touch_and_webhooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, environment variables, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CRM automation steps and command examples that require user-provided GoHighLevel, Habilis, Meta, or webhook credentials.]

## Skill Version(s):

1.0.3 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
