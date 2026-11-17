## Description:

This skill helps an agent manage a Miaoxiang simulated stock portfolio by querying positions, balances, orders, trade history, and submitting or canceling simulated A-share buy and sell orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to operate and inspect a simulated A-share portfolio, including holdings, cash, orders, and trade history. It can also prepare API-backed simulated buy, sell, and cancel actions after the exact requested action is confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit or cancel simulated trades.

Mitigation: Require clear confirmation of the exact action, stock code, quantity, price, and order identifier before allowing buy, sell, or cancel requests.

Risk: The API key is sent to a configurable API URL.

Mitigation: Keep MX_API_URL set to the documented HTTPS service unless the endpoint is explicitly trusted, and use a limited or revocable API key when available.

Risk: Account and order responses are saved locally as raw JSON.

Mitigation: Treat the OpenClaw output directory as sensitive, avoid sharing raw response files, and remove them when they are no longer needed.

Risk: Simulated trading workflows may be mistaken for real-money trading or investment advice.

Mitigation: Use the skill only for simulated account operations and do not rely on its outputs as investment advice or real trading authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqk000/skills/eastmoney-stock-simulator)
- [Publisher profile](https://clawhub.ai/user/qqk000)
- [Miaoxiang simulated account setup](https://dl.dfcfs.com/m/itc4)
- [Default simulation API base URL](https://mkapi2.dfcfs.com/finskillshub)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text summaries and raw JSON files, with Markdown documentation and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script saves text summaries and raw JSON responses under /root/.openclaw/workspace/mx_data/output/ using the mx_stock_simulator_ filename prefix.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
