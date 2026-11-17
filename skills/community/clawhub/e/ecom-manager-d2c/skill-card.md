## Description:

AI ecommerce operations manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and developers use this skill to automate store operations across inventory, pricing, content, ads, analytics, competitor monitoring, and chat-driven task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live store, advertising, messaging, and content systems.

Mitigation: Require explicit store-owner approval before every price, inventory, content, discount, messaging, and ad-spend change.

Risk: Connected ecommerce and messaging integrations may expose sensitive credentials or customer and store data.

Mitigation: Use least-privilege API tokens, store tokens securely, connect only trusted messaging channels with verified identities, and rotate credentials according to store policy.

Risk: Advertising automation and competitor monitoring can create spend, compliance, or terms-of-service risk.

Mitigation: Set budget and rate limits outside the agent and confirm competitor monitoring complies with applicable terms and laws.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhishekj9621/skills/ecom-manager-d2c)
- [Integrations](artifact/integrations.md)
- [Available Tools](artifact/tools.md)
- [Workflows](artifact/workflows.md)
- [Chat Commands](artifact/commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown or structured text with proposed ecommerce actions, reports, and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Critical store, advertising, messaging, and content changes require explicit owner approval.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
