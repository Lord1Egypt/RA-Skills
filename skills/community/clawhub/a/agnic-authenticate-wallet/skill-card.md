## Description: <br>
Authenticates an Agnic wallet through browser OAuth or a headless API token for CLI, CI, server, or agent environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to check Agnic wallet authentication, connect through browser OAuth, configure AGNIC_TOKEN for headless use, verify status, or log out. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens or OAuth credentials can grant access to an Agnic wallet. <br>
Mitigation: Prefer browser OAuth or a secure secret store for AGNIC_TOKEN, and avoid putting token values in shared terminals, shell history, logs, or transcripts. <br>
Risk: OAuth approval may include wallet spending limits. <br>
Mitigation: Review the account, wallet, and spending limits before approving access, and log out or revoke tokens when access is no longer needed. <br>


## Reference(s): <br>
- [Agnic API token settings](https://app.agnic.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user-provided Agnic credentials or OAuth approval.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
