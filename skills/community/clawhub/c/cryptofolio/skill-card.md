## Description: <br>
CryptoFolio helps users record crypto holdings, trades, finance products, transfers, and accounts through natural-language commands, with CSV/Excel export support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChristinaFanxy](https://clawhub.ai/user/ChristinaFanxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw users use cryptofolio to track crypto portfolio activity, maintain local or Cloudflare-synced records, view asset summaries, and export portfolio reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages sensitive crypto portfolio and transaction data locally and can sync it to a Cloudflare Worker. <br>
Mitigation: Use local-only mode unless sync is required, protect the Cloudflare token with a strong unique value, and avoid committing or sharing config files. <br>
Risk: The local visualization server exposes portfolio data while it is running. <br>
Mitigation: Start the server only when needed, use it on a trusted machine/network, and stop it after viewing charts or reports. <br>
Risk: AI parsing can send prompts, uploaded files, and API keys directly to the selected AI provider. <br>
Mitigation: Review provider terms before enabling AI parsing and avoid uploading screenshots or files that contain secrets or data you do not want sent to that provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ChristinaFanxy/cryptofolio) <br>
- [Project homepage from ClawHub metadata](https://github.com/ChristinaFanxy/CryptoFolio-Skill) <br>
- [CryptoFolio web app](https://christinafanxy.github.io/CryptoFolio-Skill/) <br>
- [Cloudflare Worker deployment guide](cloudflare-worker/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese text responses with shell commands, local JSON data, and CSV/Excel report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write data and configuration under ~/.openclaw/data, synchronize data to a user-provided Cloudflare Worker, start a local HTTP visualization server, and export reports.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
