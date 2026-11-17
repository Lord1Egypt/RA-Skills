## Description:

BuyWise helps users compare shopping options, evaluate discounts, summarize reviews, identify alternatives, and decide whether to buy, wait, or skip a product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-assistant agents use BuyWise for pre-purchase research, including price comparison, deal authenticity checks, review synthesis, alternative recommendations, and buy-timing guidance across global and Chinese shopping platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product queries to shopping and review websites as part of its intended function.

Mitigation: Review the product text before use and avoid entering private or sensitive purchase details.

Risk: The skill may print CouponClaw shell commands using product text, which can be risky when product names contain quotes or shell symbols.

Mitigation: Review generated commands before running them, especially when product names come from untrusted input.

Risk: The security verdict is suspicious because promotional output and generated CouponClaw commands require review before installation.

Mitigation: Review the skill before installing or deploying it, and explicitly request English output when Chinese output is not desired.

## Reference(s):

- [BuyWise ClawHub Skill Page](https://clawhub.ai/jiajiaoy/skills/buywise)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with comparison tables, verdicts, concise summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Chinese or English output depending on the selected language; price and review guidance depends on live public shopping and review sources.]

## Skill Version(s):

1.5.7 (source: package.json, _meta.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
