## Description:

家庭返利统一管理工具，聚合全家人的购物返利账户，统一追踪、统一提现，帮全家省钱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Families and household administrators use this skill to coordinate rebate-account tracking, purchase assistance, rebate summaries, and withdrawals across family members.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to manage family members' rebate accounts, orders, and withdrawals without clear consent controls.

Mitigation: Use only after every participating family member has explicitly agreed to account linking, order tracking, proxy purchasing, and withdrawals.

Risk: Proxy purchasing or moving rebate funds can affect another person's account or money.

Mitigation: Require clear confirmation before placing orders, changing account access, or withdrawing rebate funds.

Risk: Family account management may expose credentials or sensitive order data.

Mitigation: Do not casually share or store relatives' credentials, and limit access to the information needed for the agreed rebate task.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown family rebate report with member savings, pending rebate, withdrawable balance, and cumulative savings fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
