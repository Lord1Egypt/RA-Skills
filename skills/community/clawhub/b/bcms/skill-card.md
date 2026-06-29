## Description: <br>
BCMS is a headless CMS skill for coding agents that guides building with the @thebcms/client SDK for templates, entries, groups, widgets, media, functions, webhooks, API keys, and permissions, and operating content through the BCMS Model Context Protocol server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bcms](https://clawhub.ai/user/bcms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to build BCMS-backed applications, model content, integrate frameworks such as Next.js, Nuxt, Astro, Svelte, Gatsby, and Vite, and operate BCMS content through MCP when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses BCMS API and MCP credentials, including keys that can be write-capable. <br>
Mitigation: Use dedicated least-privilege BCMS keys, store them in secure local or user configuration, and never commit keys to source control or expose admin keys in browsers. <br>
Risk: MCP operations can change or delete entries, templates, groups, widgets, and media. <br>
Mitigation: Review destructive or schema-changing actions before production use, inspect usage where supported, and plan migrations for content-model changes. <br>
Risk: Webhook and function integrations can introduce replay, authorization, or idempotency issues. <br>
Mitigation: Verify webhook signatures, validate timestamps, use scoped function permissions, and design handlers to be idempotent. <br>


## Reference(s): <br>
- [BCMS ClawHub listing](https://clawhub.ai/bcms/bcms) <br>
- [BCMS agent setup guide](https://thebcms.com/agents) <br>
- [BCMS MCP documentation](https://thebcms.com/docs/mcp) <br>
- [BCMS integration guides](https://thebcms.com/docs/integrations) <br>
- [BCMS API basics](references/bcms-api-basics.md) <br>
- [BCMS MCP reference](references/mcp.md) <br>
- [BCMS permissions](references/permissions.md) <br>
- [BCMS templates](references/templates.md) <br>
- [BCMS entries](references/entries.md) <br>
- [BCMS framework integrations](references/frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, shell, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include BCMS SDK patterns, MCP operation guidance, environment variable recommendations, and content-modeling steps.] <br>

## Skill Version(s): <br>
1.3.2 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
