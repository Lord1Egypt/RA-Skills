## Description:

Amazon PPC Campaign helps sellers build new Amazon advertising campaign blueprints or optimize existing campaigns with keyword grouping, ACoS calculations, bid adjustments, negative keywords, and action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to plan launch campaigns, audit campaign performance, calculate break-even and target ACoS, and produce Seller Central-ready optimization steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to run a bundled competitor-fetch shell script or make Amazon web requests.

Mitigation: Require explicit user approval before running the script or making web requests, and review the target ASINs and marketplace first.

Risk: Recurring reminder guidance could create persistent scheduled work without enough user intent.

Mitigation: Create reminders only after the user explicitly asks for them and confirms the cadence.

Risk: Campaign recommendations may rely on estimates or user-provided reports rather than direct Seller Central data.

Mitigation: Label assumptions clearly and have the seller review recommendations against Seller Central before changing bids, budgets, or negatives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-ppc-campaign)
- [Amazon Keyword Research skill](https://github.com/nexscope-ai/Amazon-Skills/tree/main/amazon-keyword-research)
- [Amazon Listing Optimization skill](https://github.com/nexscope-ai/Amazon-Skills/tree/main/amazon-listing-optimization)
- [Nexscope](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with campaign setup tables, action plans, calculations, and inline shell commands when competitor fetching is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ACoS calculations, bid adjustment tables, negative keyword lists, campaign blueprints, and week-by-week optimization plans.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
