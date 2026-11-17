## Description:

全球水果价格收集与查询。管理水果池，自动采集榴莲/荔枝/樱桃等水果每日批发价，支持国内外报价，RMB/公斤换算。Fruit price tracker for global fruits, wholesale market data, agricultural commodity prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Fruit Pi to manage a fruit watchlist, collect current wholesale fruit prices from configured or discovered sources, normalize prices to RMB per kilogram, and present concise price summaries with source context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and repeatedly fetch unvalidated user-added or web-discovered price-source URLs.

Mitigation: Review source URLs before adding them, remove unexpected sources from the fruit pool, and avoid internal, local, or otherwise sensitive URLs.

Risk: Casual trigger phrases can initiate collection behavior that fetches configured sources.

Mitigation: Prefer explicit commands such as list, refresh, add, and remove so collection happens only when intended.

## Reference(s):

- [Fruit Pi on ClawHub](https://clawhub.ai/kobenfang/skills/fruit-pi)
- [kobenfang publisher profile](https://clawhub.ai/user/kobenfang)
- [Frankfurter exchange-rate API](https://api.frankfurter.app/latest?from=USD)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style price summary with concise text, source labels, and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local fruit-pool JSON file and cache exchange-rate data during collection.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
