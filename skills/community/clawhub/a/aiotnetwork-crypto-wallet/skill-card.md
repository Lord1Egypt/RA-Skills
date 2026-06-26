## Description: <br>
Discover supported cryptocurrencies, generate deposit addresses, and withdraw crypto to external wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External wallet users and agents use this skill to list supported crypto assets, create deposit addresses, quote withdrawals, initiate withdrawals, and confirm pending withdrawals with a transaction PIN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Withdrawals through the authenticated wallet API can be irreversible if the user chooses the wrong coin, network, destination address, amount, or fee quote. <br>
Mitigation: Require the user to manually verify the coin, network, destination address, amount, fee quote, and withdrawal confirmation before confirming a withdrawal. <br>
Risk: The configured API base URL may point to a development or unverified endpoint. <br>
Mitigation: Install only after verifying the AIOT wallet provider and AIOT_API_BASE_URL, and do not use real funds against development or unverified endpoints. <br>
Risk: The skill handles authenticated wallet operations and a transaction PIN. <br>
Mitigation: Verify a valid bearer token before authenticated calls, request the transaction PIN fresh for each confirmation, and never cache, log, or persist secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork-crypto-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/D9m1n1c) <br>
- [AIOT wallet API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with API request details and user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL endpoint configuration and authenticated wallet API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
