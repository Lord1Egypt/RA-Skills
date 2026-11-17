## Description:

EU compliance enforcement for AI agents covering NIS2, GDPR, and ISO 27001, using an organisation profile to guide data residency, supplier, secret-blocking, audit logging, and risk-appetite checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkerkhofs](https://clawhub.ai/user/pkerkhofs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and compliance staff use this skill to onboard an organisation profile and make agents flag or block compliance-relevant actions in code generation, cloud deployment, data export, supplier onboarding, incident handling, and NIS2/GDPR/ISO 27001 assessment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad compliance enforcement may cause the agent to inspect or apply sensitive organisational profile data outside explicit compliance workflows.

Mitigation: Restrict use to explicit compliance workflows and store profiles in a dedicated access-controlled file rather than in system prompts, custom instructions, shared memory, or broad project context.

Risk: Audit, cloud sync, ticketing, or observability behavior can move compliance records to external systems.

Mitigation: Keep these integrations disabled until a human approves the destination, fields, retention period, redaction rules, and access controls.

Risk: Third-party package or MCP server references can introduce supply-chain or external data-flow risk.

Mitigation: Pin and review third-party packages and MCP servers, then verify supplier approval and data-residency status against the organisation profile before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pkerkhofs/skills/eu-compliance)
- [complisec project page](https://skills.eye.security/eu-compliance/)
- [NIS2 gap analysis questionnaire details](skills/nis2-gap-analysis/references/questionnaire-details.md)
- [Audit logging code generation guide](skills/audit-logging/references/logging-guide.md)
- [Data sensitivity pattern index](skills/data-sensitivity/references/pattern-index.md)
- [EU incident reporting directory](skills/incident-management/references/eu-reporting-directory.md)
- [NIS2 Directive on EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2555)
- [GDPR on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679)
- [DORA on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/2554)
- [AI Act on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, code snippets, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local compliance profile, audit, incident, change, vendor, and assessment records when the host agent has file access; the NIS2 applicability helper requires Python 3.10+.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
