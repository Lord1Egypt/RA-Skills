## Description:

Multi-platform e-commerce automation that uses Brave Browser CDP to search products and add them to cart on Taobao and JD, favorite them on Pinduoduo, or mark them as wanted on Xianyu, stopping before checkout or payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping-assistant agents use this skill to navigate supported e-commerce sites, inspect search results, open product detail pages, and perform cart, favorite, or wanted actions with user oversight. It is not intended for price comparison, checkout, payment, product recommendation, or order management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates actions in logged-in shopping accounts, including cart, favorite, wanted, and possible chat flows.

Mitigation: Use a dedicated Brave profile or tab with accounts approved for automation, and require explicit user confirmation before any account-changing action.

Risk: Search terms and detail URLs can influence browser navigation and page actions.

Mitigation: Avoid attacker-supplied search terms or detail URLs, and inspect the destination page with screenshots and page text before acting.

Risk: The Taobao flow relies on a token-based API call and security evidence flags unsafe interpolation patterns.

Mitigation: Fix the token handling and interpolation patterns before normal use, and review generated commands before execution.

## Reference(s):

- [Platform Guides](references/platform-guides.md)
- [Platform Selectors](references/platform-selectors.md)
- [Experience Log](references/experience-log.md)
- [ClawHub Skill Page](https://clawhub.ai/mayf3/skills/add-to-cart)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with inline bash and JavaScript snippets; shell script output is terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill depends on a running Brave Browser remote debugging session and the brave-browser-agent CDP helper.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
