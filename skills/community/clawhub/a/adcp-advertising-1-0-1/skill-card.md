## Description:

AdCP Advertising helps agents discover ad inventory, create and update media buys, manage creatives, target audiences, and monitor campaign performance through natural-language advertising workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dujch](https://clawhub.ai/user/dujch)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, agencies, media buyers, e-commerce brands, startups, and developers use this skill to plan, launch, adjust, and measure advertising campaigns across display, video, CTV, audio, native, and other channels. It supports AdCP workflows for campaign discovery, media buying, creative management, targeting, delivery reporting, and budget optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign launches, budget changes, pause/resume actions, and creative reassignment can affect real ad spend or delivery.

Mitigation: Use the test agent or a sandbox first, and require explicit human confirmation for every campaign launch, budget change, pause/resume action, and creative reassignment.

Risk: The shared test token is public and unsuitable for production advertising accounts.

Mitigation: Do not reuse the shared test token for real accounts; configure production credentials issued by each sales agent.

Risk: Creative uploads, targeting overlays, and budget settings can fail validation or create unintended audience reach.

Mitigation: Validate creative formats, targeting fields, budget minimums, and pending approval status before execution, then monitor delivery after changes.

## Reference(s):

- [AdCP Documentation](https://docs.adcontextprotocol.org)
- [AdCP Documentation Index](https://docs.adcontextprotocol.org/llms.txt)
- [AdCP Media Buy Protocol](https://docs.adcontextprotocol.org/docs/media-buy/)
- [AdCP Task Reference](https://docs.adcontextprotocol.org/docs/media-buy/task-reference/)
- [AdCP Quick Reference](https://docs.adcontextprotocol.org/docs/media-buy/quick-reference)
- [AdCP Creative Protocol](https://docs.adcontextprotocol.org/docs/creative/)
- [AdCP Targeting Documentation](https://docs.adcontextprotocol.org/docs/media-buy/advanced-topics/targeting)
- [ClawHub Skill Page](https://clawhub.ai/dujch/skills/adcp-advertising-1-0-1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AdCP task names, endpoint URLs, campaign IDs, budgets, targeting fields, and creative metadata supplied by the user or agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
