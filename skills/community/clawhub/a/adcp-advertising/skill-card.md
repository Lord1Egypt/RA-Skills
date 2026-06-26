## Description: <br>
Helps agents discover ad inventory, create and manage advertising campaigns, upload creatives, adjust targeting and budgets, and monitor campaign performance through natural language workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edyyy62](https://clawhub.ai/user/edyyy62) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing teams, media buyers, agencies, e-commerce brands, and startups use this skill to automate media buying, campaign launch, creative management, targeting, reporting, and performance optimization across advertising channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-driven campaign launches and budget changes can affect real advertising spend. <br>
Mitigation: Require explicit human approval for campaign creation, budget changes, launch or resume actions, creative uploads, and targeting changes; set spend limits and use test endpoints first. <br>
Risk: Production credentials or public test tokens can be misused if handled casually. <br>
Mitigation: Do not reuse the public test token for production, and connect production AdCP credentials only after approval and credential controls are in place. <br>
Risk: Audience, customer, or regulated-category targeting data may be sensitive. <br>
Mitigation: Avoid sending sensitive targeting data unless legal and platform-policy requirements are satisfied. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edyyy62/adcp-advertising) <br>
- [Official AdCP Documentation](https://docs.adcontextprotocol.org) <br>
- [Official AdCP Repository](https://github.com/adcontextprotocol/adcp) <br>
- [AdCP Documentation Index](https://docs.adcontextprotocol.org/llms.txt) <br>
- [AdCP Media Buy Task Reference](https://docs.adcontextprotocol.org/docs/media-buy/task-reference/) <br>
- [Skill Guide](SKILL.md) <br>
- [API Reference](REFERENCE.md) <br>
- [Examples](EXAMPLES.md) <br>
- [Targeting Guide](TARGETING.md) <br>
- [Creative Guide](CREATIVE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown and natural-language responses with inline code, commands, configuration details, campaign identifiers, and performance summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce campaign, creative, targeting, budget, and reporting instructions that should be reviewed before use with production advertising accounts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
