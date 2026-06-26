## Description: <br>
Auto.dev – Automotive Data helps agents use Auto.dev APIs, MCP tools, CLI commands, and SDK methods for VIN decoding, vehicle listings, photos, specs, recalls, payments, interest rates, OEM build data, and plate-to-VIN workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryant22](https://clawhub.ai/user/bryant22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automotive workflow builders use this skill to have agents search vehicle listings, decode and enrich VINs, retrieve photos, specs, recalls, payments, taxes, and ownership costs, and scaffold Auto.dev-powered apps and integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct API workflows may expose Auto.dev API keys if keys are pasted into chat, embedded in URLs, logged, or placed in client-side code. <br>
Mitigation: Prefer OAuth-backed CLI or MCP flows where available; otherwise keep API keys in environment variables or a secret store, use authorization headers when supported, and avoid putting secrets in chat, URLs, logs, or browser-delivered code. <br>
Risk: VIN, plate, listing, and financing workflows can involve sensitive vehicle or customer-adjacent data and may forward that data to integrations such as webhooks, Google Sheets, Slack, Zapier, or email. <br>
Mitigation: Review integrations before production use, require appropriate user consent and privacy notices, allowlist callback destinations, minimize logged data, and define retention and deletion controls. <br>
Risk: Some Auto.dev endpoints and plan upgrades incur per-call or subscription charges, and batch or chained workflows can multiply cost. <br>
Mitigation: Estimate cost before batch or chained operations, warn before high-cost endpoints such as OEM build data or plate-to-VIN, and require explicit user confirmation for material spend. <br>
Risk: Generated app, webhook, alert, and export examples may need hardening before deployment. <br>
Mitigation: Review generated code for authentication, authorization, input validation, callback allowlists, secret handling, logging, and operational monitoring before using it in production. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bryant22/auto-dev) <br>
- [Auto.dev CLI, MCP, and SDK documentation](https://docs.auto.dev/v2/cli-mcp-sdk) <br>
- [Auto.dev API documentation](https://docs.auto.dev/) <br>
- [Auto.dev pricing](https://auto.dev/pricing) <br>
- [Skill homepage](https://github.com/drivly/auto-dev-skill) <br>
- [Glama MCP server listing](https://glama.ai/mcp/servers/drivly/auto-dev-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, API examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CSV or JSON export guidance for larger vehicle data results when requested.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata; artifact SKILL.md frontmatter is 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
