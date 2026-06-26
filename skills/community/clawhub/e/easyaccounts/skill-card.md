## Description: <br>
Family finance manager for EasyAccounts that lets an agent record, query, update, transfer, summarize, and export personal bookkeeping data through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingheyang](https://clawhub.ai/user/qingheyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and EasyAccounts users use this skill to connect an agent to a self-hosted personal bookkeeping server for expense entry, transaction lookup, updates, transfers, statistics, reports, and system notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change configured EasyAccounts financial records. <br>
Mitigation: Install only for trusted EasyAccounts servers and review add, update, batch, and transfer actions before allowing them. <br>
Risk: Credentials and authentication tokens may grant access to personal bookkeeping data. <br>
Mitigation: Protect ~/.openclaw/.env and ~/.config/easyaccounts/token, and configure EASYACCOUNTS_URL only for the intended server. <br>
Risk: Generated Excel exports remain on the EasyAccounts server for later retrieval. <br>
Mitigation: Handle exported files according to the server operator's data retention and access controls. <br>


## Reference(s): <br>
- [ClawHub Easyaccounts release](https://clawhub.ai/qingheyang/easyaccounts) <br>
- [EasyAccounts project](https://github.com/QingHeYang/EasyAccounts) <br>
- [EasyAccounts skill source path](https://github.com/QingHeYang/EasyAccounts/tree/main/skills/easyaccounts) <br>
- [EasyAccounts issue tracker](https://github.com/QingHeYang/EasyAccounts/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update EasyAccounts records and may request Excel report generation on the configured EasyAccounts server.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
