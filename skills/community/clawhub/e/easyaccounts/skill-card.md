## Description:

EasyAccounts is a family finance manager skill that connects natural-language agent requests to an EasyAccounts personal bookkeeping system for recording, querying, batch entry, internal transfers, flow updates, income and expense statistics, annual analysis, Excel export, and system notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingheyang](https://clawhub.ai/user/qingheyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an EasyAccounts deployment use this skill to manage household bookkeeping through an agent, including adding and updating transactions, querying account flows, summarizing income and expenses, exporting Excel reports, and checking system notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send credentials and private financial data to an EasyAccounts server, including over plaintext HTTP when configured that way.

Mitigation: Install only for EasyAccounts servers the user controls or trusts, prefer HTTPS, and avoid Internet-exposed HTTP endpoints.

Risk: Reusable authentication material and optional credentials may exist locally in token or environment files.

Mitigation: Avoid passing passwords on the command line, protect the environment file with restrictive permissions, and treat saved tokens as sensitive.

Risk: The skill can create or update financial records and generate server-side Excel files that contain financial data.

Mitigation: Review transaction details before execution and retrieve exported reports only through trusted EasyAccounts front-end or operations channels.

## Reference(s):

- [ClawHub Easyaccounts listing](https://clawhub.ai/qingheyang/skills/easyaccounts)
- [EasyAccounts skill source](https://github.com/QingHeYang/EasyAccounts/tree/main/skills/easyaccounts)
- [EasyAccounts project](https://github.com/QingHeYang/EasyAccounts)
- [EasyAccounts issues](https://github.com/QingHeYang/EasyAccounts/issues)
- [jq download](https://jqlang.github.io/jq/download/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell-command-backed JSON results and financial summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update EasyAccounts records, query financial flows, and request server-side Excel exports.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
