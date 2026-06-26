## Description: <br>
Asset Management helps users record crypto holdings, trades, finance products, transfers, and account data through natural-language workflows and export CSV or Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChristinaFanxy](https://clawhub.ai/user/ChristinaFanxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to maintain personal crypto portfolio records, review holdings and transactions, configure optional Cloudflare sync, open a local dashboard, and export reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto holdings and transaction history are sensitive financial records when stored locally or in Cloudflare KV. <br>
Mitigation: Install only when that storage model is acceptable, protect the local data directory, and use a Cloudflare account and KV namespace you control. <br>
Risk: Cloud sync credentials can be exposed if real tokens are committed, pasted into shared logs, or left in shell history. <br>
Mitigation: Use a strong unique sync token, avoid storing real tokens in source files, and rotate the token if it may have been exposed. <br>
Risk: The local dashboard API can expose portfolio data while it is running. <br>
Mitigation: Run the dashboard only when needed, keep it bound to local use, and stop it after reviewing or editing portfolio data. <br>
Risk: AI parsing may send prompts, uploaded files, and API keys to the selected AI provider. <br>
Mitigation: Avoid entering unnecessary secrets or sensitive records into prompts and review provider data-handling terms before using AI-assisted parsing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChristinaFanxy/crypto-folio) <br>
- [Project homepage](https://github.com/ChristinaFanxy/CryptoFolio-Skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and concise text with command examples and generated CSV or Excel files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON portfolio data, cloud sync configuration, exported reports, and local dashboard responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
