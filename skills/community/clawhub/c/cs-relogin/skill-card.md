## Description: <br>
Fast OpenAI Codex account switch for OpenClaw via the local cs command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anjun](https://clawhub.ai/user/anjun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to switch the local OpenAI Codex account with the trusted `cs relogin` command, complete callback-based login, and inspect account status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local account-switching command that can change the active Codex/OpenClaw account. <br>
Mitigation: Use it only when you intend to switch accounts and have confirmed that `cs` is the trusted local command on the machine. <br>
Risk: OAuth callback URLs or codes are sensitive and can complete a login flow. <br>
Mitigation: Provide callback material only after personally initiating the login and expecting the account switch; do not expose full tokens or secrets in responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anjun/cs-relogin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a login URL, callback next step, command stderr on failure, relogin status, gateway restart status, and active account summary; must not expose full tokens or secrets.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
