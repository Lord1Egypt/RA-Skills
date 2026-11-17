## Description:

自动客服应答虾 helps agents build and operate a Chinese customer-service bot for intent classification, FAQ matching, response templating, multi-turn handling, and human handoff decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External support teams, operators, and developers use this skill to configure FAQ knowledge, intent rules, reply templates, and service commands for automated customer support workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service can expose an unauthenticated customer-service endpoint if deployed beyond localhost.

Mitigation: Keep the service bound to localhost for testing, and add authentication, authorization, network controls, and production hardening before any external deployment.

Risk: FAQ import handling may be unsafe with untrusted file names or untrusted source files.

Mitigation: Review import scripts before use, restrict imports to trusted files, validate file paths and formats, and avoid running the scripts with elevated privileges.

Risk: Real customer conversations may contain personal or sensitive information.

Mitigation: Define privacy, retention, access-control, and logging rules before using the skill with customer data.

Risk: Unpinned runtime dependencies can change behavior or introduce vulnerable packages over time.

Mitigation: Install dependencies in a virtual environment with pinned versions and review dependency updates before deployment.

## Reference(s):

- [FAQ Knowledge Base](references/faq-database.md)
- [Intent Rules](references/intent-rules.md)
- [Response Templates](references/response-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/auto-customer-service-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration-oriented text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces customer-service replies, FAQ and intent-rule guidance, service-management commands, and handoff recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
