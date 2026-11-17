## Description:

将用户自愿提供的家庭库存、消耗量、预算和饮食限制整理为可核对的补货清单、购物对照表及待确认事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Households use this skill to plan restocking from their own inventory, consumption estimates, budget and dietary restrictions, while reviewing uncertainties before any purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household information or credentials may be exposed through optional external uploads.

Mitigation: Share only approved, necessary household data; never provide passwords, tokens, cookies, verification codes or full identity documents.

Risk: Optional model calls or purchases may incur costs or make unwanted changes.

Mitigation: Confirm current prices, upload scope and spending limit before paid calls; require separate user approval before orders, payments or other external changes.

Risk: Unverified stock, dietary substitutions or prices could make the shopping list unsafe or inaccurate.

Mitigation: Keep unknown quantities and prices marked for review, honor allergy restrictions, and verify live prices against a network source.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-household-restock)
- [Household restocking workflow](references/workflow-48.md)
- [Result and evidence contract](references/output-contract.md)
- [Optional AI-HIVE connection](references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [CSV restocking list, shopping comparison and items for confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-linked estimates; unknown values remain marked for review. No automatic ordering or payment.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
