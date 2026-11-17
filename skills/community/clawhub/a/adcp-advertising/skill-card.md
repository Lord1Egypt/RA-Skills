## Description:

Ad Context Protocol (AdCP) Advertising helps agents discover ad inventory, create and update media buys, manage creatives, monitor delivery, and optimize campaign performance across display, video, CTV, audio, native, and DOOH channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edyyy62](https://clawhub.ai/user/edyyy62)

### License/Terms of Use:

MIT

## Use Case:

Marketing teams, media buyers, agencies, e-commerce operators, startups, and developers use this skill to plan, launch, adjust, and monitor advertising campaigns through natural language workflows and AdCP API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can create campaigns, change budgets, pause or resume media buys, reassign creatives, and optimize spend in ways that may spend or reallocate real advertising budget.

Mitigation: Require explicit human approval for every campaign creation, budget change, pause or resume action, creative reassignment, and automated optimization before connecting production ad accounts.

Risk: Production advertising endpoints require bearer tokens and account-specific credentials.

Mitigation: Store production tokens in a secret manager or environment variables, keep the public test token limited to testing, and enable budget caps and audit logging before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edyyy62/skills/adcp-advertising)
- [Official AdCP Documentation](https://docs.adcontextprotocol.org)
- [Official AdCP Repository](https://github.com/adcontextprotocol/adcp)
- [AdCP Documentation Index](https://docs.adcontextprotocol.org/llms.txt)
- [Media Buy Protocol](https://docs.adcontextprotocol.org/docs/media-buy/)
- [Media Buy Task Reference](https://docs.adcontextprotocol.org/docs/media-buy/task-reference/)
- [AdCP Quick Reference](https://docs.adcontextprotocol.org/docs/media-buy/quick-reference)
- [Creative Protocol](https://docs.adcontextprotocol.org/docs/creative/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with natural language instructions, API examples, JSON snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose actions that affect live advertising campaigns, budgets, creatives, targeting, and performance optimization.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
