## Description: <br>
Guides agents and developers through integrating PayRam as a self-hosted crypto and stablecoin payment gateway for applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to assess projects, configure PayRam, generate payment and webhook integration code, and scaffold applications that accept crypto or stablecoin payments without hosted payment intermediaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to run a third-party MCP helper and generate payment-related code. <br>
Mitigation: Inspect the PayRam MCP repository, prefer a pinned commit or release, and run it in a development environment before production use. <br>
Risk: Generated payment, webhook, payout, and environment files can affect funds flow or application secrets if applied without review. <br>
Mitigation: Review generated files and configuration before deploying them to production. <br>


## Reference(s): <br>
- [PayRam website](https://payram.com) <br>
- [PayRam GitHub](https://github.com/PayRam) <br>
- [PayRam helper MCP server](https://github.com/PayRam/payram-helper-mcp-server) <br>
- [PayRam setup skill](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, framework scaffolding guidance, and configuration templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated payment, webhook, payout, and environment files should be reviewed before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
