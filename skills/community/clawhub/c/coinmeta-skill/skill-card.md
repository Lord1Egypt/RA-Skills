## Description:

Fetch latest cryptocurrency newsflashes and market updates using CoinMeta API with keyword search and pagination support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[semithin](https://clawhub.ai/user/semithin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query CoinMeta for cryptocurrency newsflashes, market updates, article lists, and keyword-based article or news searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends COINMETA_API_KEY to CoinMeta when the documented API calls are made.

Mitigation: Install and use the skill only when the agent is expected to query CoinMeta, and scope the API key according to the account's operational requirements.

Risk: The broad 'market updates' trigger could invoke the skill for requests that are not explicitly about CoinMeta or cryptocurrency news.

Mitigation: Tighten trigger usage in the host agent or require explicit CoinMeta or crypto-news intent before calling the skill.

## Reference(s):

- [CoinMeta API base URL](https://api.coinmeta.com)
- [CoinMeta skill page](https://clawhub.ai/semithin/skills/coinmeta-skill)
- [Publisher profile](https://clawhub.ai/user/semithin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with curl examples and formatted cryptocurrency news or article summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pagination, keyword search, readable timestamp conversion, and HTML stripping for newsflash content.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
