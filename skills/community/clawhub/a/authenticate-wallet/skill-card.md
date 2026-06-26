## Description: <br>
Authenticate Wallet helps agents check wallet authentication status and guide an email OTP login using the npx awal CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to authenticate a payments wallet before wallet operations such as checking status, balance, or address. It provides a guided email OTP flow for signing in when wallet operations fail with authentication errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through email OTP wallet login, which may expose an email address, one-time code, or wallet session. <br>
Mitigation: Confirm each login attempt yourself, prefer entering OTPs directly instead of handing them to the agent, and treat any email address, OTP, or resulting wallet session as sensitive. <br>


## Reference(s): <br>
- [Authenticate Wallet on ClawHub](https://clawhub.ai/0xRAG/authenticate-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are limited to npx awal@latest status, auth, balance, address, and show operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
