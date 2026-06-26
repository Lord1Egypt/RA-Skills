## Description: <br>
全球水果价格收集与查询。管理水果池，自动采集榴莲/荔枝/樱桃等水果每日批发价，支持国内外报价，RMB/公斤换算。Fruit price tracker for global fruits, wholesale market data, agricultural commodity prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a local fruit watchlist, collect configured fruit-price data, supplement missing prices through search, and present normalized RMB/kg price summaries with original-currency context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Price queries can create or update a local fruit-pool file containing the user's tracked fruit preferences. <br>
Mitigation: Use the skill for non-sensitive tracking and review or delete the fruit-pool file when stored preferences are no longer needed. <br>
Risk: Price collection may contact configured market websites, search providers, and an exchange-rate API. <br>
Mitigation: Avoid adding private or internal URLs as price sources and review configured sources before collection. <br>
Risk: Collected prices and currency conversions may be unavailable, stale, or estimated when sources fail. <br>
Mitigation: Check source labels, timestamps, and exchange-rate notes before using prices for purchasing decisions. <br>


## Reference(s): <br>
- [ClawHub Fruit Pi skill page](https://clawhub.ai/kobenfang/fruit-pi) <br>
- [Frankfurter exchange-rate API](https://api.frankfurter.app/latest?from=USD) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown fruit-price summaries with inline shell commands and JSON-backed local configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a local fruit-pool JSON file and may use external market pages, search providers, and an exchange-rate API to prepare the final user-facing summary.] <br>

## Skill Version(s): <br>
1.1.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
