## Description:

Monitor Bitget PoolX for new staking projects using r.jina.ai to bypass Cloudflare. Detect ETH, BTC, SOL and other pool launches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itonlyforfun-ai](https://clawhub.ai/user/itonlyforfun-ai)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor Bitget PoolX staking pages for active or newly launched pools and inspect status output for assets such as BTC and ETH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included billing helper uses a hardcoded SkillPay API key and under-scoped payment behavior.

Mitigation: Revoke and replace the exposed key, move billing to a server-side scoped integration, and require explicit per-charge user consent before use.

Risk: The skill sends monitoring traffic through r.jina.ai and may send billing data to SkillPay.

Mitigation: Run only in a constrained environment with explicit network allowlists and disclose the r.jina.ai and SkillPay data flows to users.

Risk: The artifact includes bitget-final.py, an alternate browser-scraping path that disables safety controls.

Mitigation: Avoid using bitget-final.py unless it is removed or hardened and reviewed before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itonlyforfun-ai/skills/bitget-poolx-monitor)
- [Publisher profile](https://clawhub.ai/user/itonlyforfun-ai)
- [Bitget PoolX page](https://www.bitget.com/events/poolx)
- [r.jina.ai Bitget PoolX endpoint](https://r.jina.ai/https://www.bitget.com/events/poolx)
- [SkillPay service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell and Python examples plus plain-text monitor status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform outbound HTTP requests to Bitget through r.jina.ai and to SkillPay when billing helpers are used.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
