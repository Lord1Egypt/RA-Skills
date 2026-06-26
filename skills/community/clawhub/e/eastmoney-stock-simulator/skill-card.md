## Description: <br>
妙想提供的股票模拟组合管理系统，支持持仓查询、买卖操作、撤单、委托查询、历史成交查询和资金查询等功能。通过安全认证的API接口实现真实交易体验。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QQK000](https://clawhub.ai/user/QQK000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage a 妙想 simulated A-share trading account, including checking positions and funds, submitting simulated buy or sell orders, canceling orders, and reviewing order history. It is not for real-money trading or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trade and cancel flows can change simulated account state, including canceling all open simulated orders from broad cancel wording. <br>
Mitigation: Use explicit buy, sell, and cancel instructions; review parsed intent and account responses before relying on the result. <br>
Risk: MX_APIKEY grants access to the simulated trading account and raw account results are saved to disk. <br>
Mitigation: Keep MX_APIKEY secret and treat the output directory as sensitive account data. <br>
Risk: Changing MX_API_URL can redirect requests away from the legitimate provider endpoint. <br>
Mitigation: Leave MX_API_URL pointed at the documented provider endpoint unless the publisher provides a trusted replacement. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/QQK000/eastmoney-stock-simulator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/QQK000) <br>
- [妙想 simulated account setup](https://dl.dfcfs.com/m/itc4) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, guidance] <br>
**Output Format:** [Console text plus saved .txt summaries and raw .json API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY and optionally MX_API_URL; writes output under /root/.openclaw/workspace/mx_data/output/.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
