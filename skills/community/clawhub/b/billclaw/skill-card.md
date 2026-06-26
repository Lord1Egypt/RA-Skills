## Description: <br>
This skill should be used when managing financial data, syncing bank transactions via Plaid/GoCardless, fetching bills from Gmail, or exporting to Beancount/Ledger formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xBinKai](https://clawhub.ai/user/xBinKai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use BillClaw to manage local financial records, sync bank transactions through Plaid or GoCardless, fetch bills from Gmail, and export accounting data to Beancount or Ledger formats. <br>

### Deployment Geography for Use: <br>
Global, with bank data integrations described for US/Canada and Europe. <br>

## Known Risks and Mitigations: <br>
Risk: BillClaw handles sensitive bank and Gmail-related data. <br>
Mitigation: Grant only the Plaid, GoCardless, or Gmail access needed for the intended workflow. <br>
Risk: Local financial data may remain in ~/.firela/billclaw/. <br>
Mitigation: Protect the local data directory and delete it when the data is no longer needed. <br>
Risk: High-trust financial workflows depend on the installed @firela packages. <br>
Mitigation: Verify npm package and source provenance before using the skill for sensitive financial records. <br>


## Reference(s): <br>
- [BillClaw ClawHub page](https://clawhub.ai/xBinKai/billclaw) <br>
- [BillClaw documentation and source](https://github.com/fire-la/billclaw) <br>
- [@firela/billclaw-openclaw npm package](https://www.npmjs.com/package/@firela/billclaw-openclaw) <br>
- [@firela npm organization](https://www.npmjs.com/org/firela) <br>
- [Plaid Dashboard](https://dashboard.plaid.com/) <br>
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces user-directed setup, sync, status, and export guidance for BillClaw integrations.] <br>

## Skill Version(s): <br>
0.5.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
