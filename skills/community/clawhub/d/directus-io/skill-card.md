## Description:

Provides Directus headless CMS guidance for setup, SDK and API usage, frontend integrations, data modeling, automations, extensions, access control, files, real-time subscriptions, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, configure, and troubleshoot Directus-backed content systems, APIs, frontend integrations, automation flows, and custom extensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples handle credentials, tokens, and deployment secrets.

Mitigation: Use scoped tokens, keep secrets in environment variables or secret stores, and avoid placing credentials in URLs or shell arguments.

Risk: Schema migration, container, and package commands can change or damage a Directus project if copied without review.

Mitigation: Review schema diffs, test changes in staging, keep backups or snapshots, and pin npx packages and container images before production use.

Risk: CMS HTML and integrations with external or AI services can expose unsafe content or private data.

Mitigation: Sanitize rendered CMS HTML and require explicit approval and privacy review before sending CMS content to third-party services.

## Reference(s):

- [Directus Skill](SKILL.md)
- [Directus + Astro Integration Guide](references/astro-integration.md)
- [Directus Data Modeling & Administration](references/data-modeling.md)
- [Directus Extensions](references/extensions.md)
- [Directus Flows & Automation](references/flows-and-automation.md)
- [Directus SDK & API Reference](references/sdk-and-api.md)
- [Directus Troubleshooting](references/troubleshooting.md)
- [Directus TypeScript Patterns](references/typescript-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline code blocks, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include example TypeScript, Astro, Docker, environment, REST, GraphQL, and Directus configuration snippets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
