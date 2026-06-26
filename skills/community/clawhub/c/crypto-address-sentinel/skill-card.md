## Description: <br>
Monitor wallet balances and on-chain activity, with alerts when balances change or specified conditions are met. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiuannnn](https://clawhub.ai/user/zhiuannnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor blockchain wallet balances and activity across supported chains, track portfolios, detect unusual activity, and monitor airdrop eligibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watched wallet addresses and alert contents may reveal sensitive portfolio or activity information. <br>
Mitigation: Treat monitored addresses and generated alerts as sensitive data and share them only with trusted systems and recipients. <br>
Risk: Webhook alerts can expose monitoring data or route notifications to an untrusted endpoint. <br>
Mitigation: Use only trusted webhook URLs and verify the destination before enabling alerts. <br>
Risk: Crypto monitoring workflows can be misused if private keys, seed phrases, or signing permissions are provided. <br>
Mitigation: Provide public wallet addresses only; do not provide private keys, seed phrases, or signing permissions. <br>


## Reference(s): <br>
- [Crypto Address Sentinel ClawHub listing](https://clawhub.ai/zhiuannnn/crypto-address-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
