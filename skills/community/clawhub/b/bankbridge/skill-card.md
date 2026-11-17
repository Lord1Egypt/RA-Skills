## Description:

Answer questions about the user's own money with live, read-only data from their connected US banks, credit cards and brokerages through the BankBridge MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakemarsh](https://clawhub.ai/user/jakemarsh)

### License/Terms of Use:

MIT-0

## Use Case:

People with connected US bank, credit card, and brokerage accounts can use this skill to review balances, spending, recurring charges, cash flow, transactions, and investment activity. It provides read-only account information and cannot move money, pay bills, or place trades.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Account balances and transaction details are sensitive financial information.

Mitigation: Keep account data in the conversation and do not paste it into other tools or services unless the user asks.

Risk: A bank may be disconnected or fail to return data, leaving totals incomplete.

Mitigation: Check and report result warnings, and state when totals cover only the banks that answered.

## Reference(s):

- [BankBridge documentation](https://bankbridge.money/docs)
- [BankBridge connector listing](https://claude.ai/directory/connectors/bankbridge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Financial summaries]

**Output Format:** [Plain text or Markdown responses with account figures, comparisons, and explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live, read-only account data; responses should surface relevant data warnings and account coverage limits.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
