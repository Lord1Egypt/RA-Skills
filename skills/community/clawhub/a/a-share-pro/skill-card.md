## Description:

A Share Pro helps agents manage a local A-share watchlist and retrieve stock quote summaries from multiple market data providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wran93409](https://clawhub.ai/user/wran93409)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to maintain A-share watchlists, run command-line quote checks, and summarize portfolio movement from third-party data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer has a path bug that can run an unintended local Python file during setup.

Mitigation: Review the installer before use, run commands manually from the skill directory when possible, and correct the script path before deployment.

Risk: Watchlists and transactions are stored as local plaintext files under ~/.openclaw/a_share.

Mitigation: Avoid storing sensitive account details, protect local file permissions, and treat backups of this directory as sensitive.

Risk: Stock symbols are sent to third-party quote providers, and one Tencent endpoint uses unauthenticated HTTP data.

Mitigation: Use the data as informational, verify important prices against trusted sources, and avoid sending symbols that reveal sensitive trading intent.

Risk: Sample analysis reports and generated summaries can be mistaken for financial advice.

Mitigation: Present outputs as informational only and require human review before making investment decisions.

## Reference(s):

- [A Share Pro ClawHub Skill Page](https://clawhub.ai/wran93409/skills/a-share-pro)
- [Declared Project Homepage](https://github.com/openclaw/skills/a-share-pro)
- [Python](https://www.python.org/)
- [Xueqiu Realtime Quote Endpoint](https://stock.xueqiu.com/v5/stock/realtime/quotec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local plaintext watchlist and transaction files; quote summaries depend on external market data providers.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
