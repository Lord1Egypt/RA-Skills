## Description:

CryptoFolio helps users record and manage cryptocurrency holdings, trades, finance products, transfers, accounts, and CSV or Excel exports through natural-language interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christinafanxy](https://clawhub.ai/user/christinafanxy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a crypto portfolio ledger through conversation, including holdings, trades, earning products, transfers, account records, local/cloud sync setup, visualization, and report export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed crypto portfolio records may be stored locally and, when sync is enabled, in a user-managed Cloudflare KV namespace.

Mitigation: Use the skill only for data you are comfortable storing in those locations, verify the sync URL, keep backups, and restrict access to the configured storage.

Risk: Cloud sync depends on a bearer token and Worker configuration chosen by the user.

Mitigation: Use a strong unique token, prefer Cloudflare secrets over hardcoded Worker tokens, and rotate the token if it may have been exposed.

Risk: The local visualization server can expose portfolio data if started on an untrusted network.

Mitigation: Run the visualization server only on trusted networks and stop it when finished.

Risk: AI-assisted entry can send user text, uploaded screenshots, documents, and API credentials to the selected AI provider.

Mitigation: Configure AI only with providers you trust, avoid paid API keys or sensitive uploads unless that data sharing is acceptable, and review parsed entries before saving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christinafanxy/skills/cryptofolio)
- [Project homepage from clawdis metadata](https://github.com/ChristinaFanxy/CryptoFolio-Skill)
- [Cloudflare Worker deployment guide](cloudflare-worker/README.md)
- [Web interface](https://christinafanxy.github.io/CryptoFolio-Skill/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with inline shell commands, configuration snippets, and generated CSV-compatible report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio data and exported reports, and may synchronize records to a user-configured Cloudflare Worker.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
