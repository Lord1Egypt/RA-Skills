## Description: <br>
Authenticate an Agnic wallet via browser OAuth or headless API token for login, wallet connection, CLI setup, or resolving authentication errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent environments use this skill to authenticate the Agnic CLI with either browser OAuth or a headless API token before running wallet-dependent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens or OAuth credentials could be exposed through logs, shared shells, or persistent local credential storage. <br>
Mitigation: Keep AGNIC_TOKEN out of logs and shared shells, prefer pinned CLI versions for production automation, review OAuth spending limits before approval, and run logout or remove ~/.agnic/config.json when local credentials should no longer be stored. <br>


## Reference(s): <br>
- [Agnic App](https://app.agnic.ai) <br>
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/agnicpay-authenticate-wallet) <br>
- [Agnic publisher profile](https://clawhub.ai/user/agnicpay-prog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authentication mode selection, token handling guidance, status verification commands, logout instructions, and expected CLI output examples.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
