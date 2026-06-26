## Description: <br>
Directus.io Headless CMS helps agents answer questions about Directus setup, SDK and API usage, frontend integrations, Flows and automations, extensions, data modeling, permissions, file management, realtime features, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, and troubleshoot Directus-backed content systems, including CMS data models, API clients, framework integrations, automations, and extensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example Directus authentication and integration snippets may expose secrets or tokens if copied directly into production. <br>
Mitigation: Keep secrets server-side, avoid tokens in URLs, use least-privilege tokens, and review environment variables before deployment. <br>
Risk: Cookie-based authentication examples can be unsafe without correct browser and server protections. <br>
Mitigation: Add SameSite and CSRF protections, configure CORS carefully, and validate cookie behavior in the target deployment environment. <br>
Risk: Schema, automation, webhook, and AI-service examples can affect production data or send content to external services. <br>
Mitigation: Review schema changes, back up production data, and confirm what content is sent to OpenAI, translation APIs, webhooks, or search services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/directus-io) <br>
- [SDK & API](references/sdk-and-api.md) <br>
- [Astro Integration](references/astro-integration.md) <br>
- [TypeScript Patterns](references/typescript-patterns.md) <br>
- [Flows & Automation](references/flows-and-automation.md) <br>
- [Extensions](references/extensions.md) <br>
- [Data Modeling & Administration](references/data-modeling.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples should be reviewed before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
