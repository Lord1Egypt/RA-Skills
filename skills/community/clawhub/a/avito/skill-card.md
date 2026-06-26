## Description: <br>
Manage Avito.ru account, items, and messenger via API. Use for listing items, checking balance, reading chats, and getting account info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RuslanLanket](https://clawhub.ai/user/RuslanLanket) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate Avito.ru account workflows through API helper scripts, including authentication, account lookup, balance checks, listing advertisements, and listing chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Avito API credentials, bearer tokens, and account data. <br>
Mitigation: Use short-lived or least-privileged Avito credentials, avoid sharing tokens in chats or logs, and store secrets in environment variables or a secret manager when adapting the scripts. <br>
Risk: Command-line token and credential arguments may be exposed through shell history or process listings. <br>
Mitigation: Prefer prompting, environment variables, or a local secret manager instead of passing credentials directly as command-line arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RuslanLanket/avito) <br>
- [Avito API token endpoint](https://api.avito.ru/token) <br>
- [Avito account self endpoint](https://api.avito.ru/core/v1/accounts/self) <br>
- [Avito items endpoint](https://api.avito.ru/core/v1/items) <br>
- [Avito messenger chats endpoint](https://api.avito.ru/messenger/v2/accounts/{user_id}/chats) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands; scripts return JSON from Avito API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Avito client credentials or bearer tokens; Messenger API access may require an Avito subscription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
