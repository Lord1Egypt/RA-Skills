## Description: <br>
Monitor Bitget PoolX for new staking projects using r.jina.ai to bypass Cloudflare. Detect ETH, BTC, SOL and other pool launches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itonlyforfun-AI](https://clawhub.ai/user/itonlyforfun-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor Bitget PoolX for new or ongoing staking pools and surface launch status for assets such as BTC and ETH. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses r.jina.ai to proxy Bitget PoolX requests and bypass Cloudflare or anti-bot protection. <br>
Mitigation: Use it only where proxying through r.jina.ai and the related anti-bot bypass behavior are explicitly acceptable. <br>
Risk: The artifact includes live SkillPay billing code that can check balances, create payment links, and charge a user account. <br>
Mitigation: Do not run billing.py or call charge_user unless the SkillPay account, API key, billed user_id, and user-approved charge flow have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itonlyforfun-AI/bitget-poolx-monitor) <br>
- [Bitget PoolX page](https://www.bitget.com/events/poolx) <br>
- [r.jina.ai PoolX proxy endpoint](https://r.jina.ai/https://www.bitget.com/events/poolx) <br>
- [SkillPay service endpoint](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included monitor scripts print status strings such as HAS_POOLS, NO_POOLS, UNKNOWN, or ERROR.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
