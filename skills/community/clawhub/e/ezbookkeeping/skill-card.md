## Description: <br>
Use ezBookkeeping API Tools script to record new transactions, query transactions, retrieve account information, retrieve categories, retrieve tags, and retrieve exchange rate data in the self hosted personal finance application ezBookkeeping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayswind](https://clawhub.ai/user/mayswind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent run ezBookkeeping API tool scripts for querying finance data, managing accounts, categories, tags, transactions, session tokens, and exchange rates on a configured self-hosted ezBookkeeping server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify sensitive finance data on the configured ezBookkeeping server. <br>
Mitigation: Install it only for workflows where agent access to that server is intended, and use a dedicated least-privilege token. <br>
Risk: The required API token may be exposed if stored in broadly readable environment or .env files. <br>
Mitigation: Restrict token file permissions and avoid broad home-directory .env discovery where possible. <br>
Risk: The token revocation command is a session-management action that can disrupt access. <br>
Mitigation: Treat tokens-revoke as an admin or destructive command and run it only with explicit intent. <br>


## Reference(s): <br>
- [ezBookkeeping](https://ezbookkeeping.mayswind.net) <br>
- [ClawHub skill page](https://clawhub.ai/mayswind/ezbookkeeping) <br>
- [Publisher profile](https://clawhub.ai/user/mayswind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and PowerShell command examples, plus API response text or tables returned by the scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EBKTOOL_SERVER_BASEURL and EBKTOOL_TOKEN to access the target ezBookkeeping server.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
