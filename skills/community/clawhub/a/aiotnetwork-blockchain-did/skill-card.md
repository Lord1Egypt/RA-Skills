## Description: <br>
Decentralized identity (DID) management, on-chain KYC status, and membership tiers with token staking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check or create a decentralized identity, complete on-chain KYC at a selected level, and inspect or upgrade membership tiers by staking tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide sensitive KYC completion and token-staking actions that may affect identity status, funds, tier eligibility, or lockup terms. <br>
Mitigation: Before KYC completion or staking, require the agent to show the exact endpoint, KYC level, token amount, account, expected tier, and reversibility or lockup terms, then get explicit user confirmation. <br>
Risk: Endpoint misconfiguration could send identity or staking actions to an unintended AIOT Network service. <br>
Mitigation: Verify AIOT_API_BASE_URL and the exact request path before any authenticated, KYC, DID creation, or staking action. <br>
Risk: Authentication tokens and transaction PINs can expose account access if reused, logged, or persisted. <br>
Mitigation: Use a valid bearer token only for the current session, ask for transaction PINs fresh when required, and never cache, log, or persist secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork-blockchain-did) <br>
- [AIOT Network API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown with API endpoint references and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL configuration and authenticated requests for protected endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
