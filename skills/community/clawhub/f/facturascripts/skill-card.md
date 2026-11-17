## Description:

Helps agents develop, debug, document, and integrate FacturaScripts 2025 ERP plugins, controllers, models, views, REST APIs, MCP servers, and business workflows using bundled Spanish technical references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joseconti](https://clawhub.ai/user/joseconti)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ERP implementers use this skill to create or modify FacturaScripts plugins, work with models, controllers, views, databases, security, translations, and draft integration code or commands for FacturaScripts deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API or MCP code may access or mutate privileged ERP data such as invoices, stock, purchases, sales, or accounting records.

Mitigation: Use least-privilege API keys, avoid full-access tokens, and review tools that create or modify ERP data before enabling them.

Risk: Examples involving remote FacturaScripts servers or destructive operations can expose credentials or damage business data if copied without review.

Mitigation: Require HTTPS for non-local servers and keep destructive examples such as DELETE or DROP TABLE behind explicit user-approved workflows.

## Reference(s):

- [Skill entrypoint](artifact/SKILL.md)
- [Skill README](artifact/README.md)
- [Architecture reference](artifact/references/architecture.md)
- [Plugin development reference](artifact/references/plugins.md)
- [Models reference](artifact/references/models.md)
- [Controllers reference](artifact/references/controllers.md)
- [Advanced controllers reference](artifact/references/controllers-advanced.md)
- [Views and widgets reference](artifact/references/views-widgets.md)
- [REST API and MCP reference](artifact/references/api.md)
- [Database reference](artifact/references/database.md)
- [Libraries reference](artifact/references/libraries.md)
- [Security reference](artifact/references/security.md)
- [Translations reference](artifact/references/translations.md)
- [Quick reference](artifact/references/quick-reference.md)
- [FacturaScripts website](https://www.facturascripts.com)
- [Jose Conti plugins](https://plugins.joseconti.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code blocks, command examples, configuration snippets, and ERP integration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; generated outputs may include privileged ERP API examples and should be reviewed before use.]

## Skill Version(s):

2025.81.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
