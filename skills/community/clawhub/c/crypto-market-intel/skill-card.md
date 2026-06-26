## Description: <br>
Crypto Market Intel fetches live cryptocurrency, DeFi, stock index, AI stock, and macro market data from public sources and prepares structured outputs for agent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avmw2025](https://clawhub.ai/user/avmw2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch current crypto, stock, DeFi, sentiment, and macro indicators, then use the resulting JSON files and analysis prompt for market intelligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public market-data services and writes local JSON files to a user-selected directory. <br>
Mitigation: Install only when those external API calls and local file writes are acceptable, and choose an output directory that does not overwrite important files. <br>
Risk: The artifact includes an optional hourly cron workflow for ongoing market-data refreshes. <br>
Mitigation: Enable the cron job only when recurring network access and local refreshes are intended, and remove the scheduled job when it is no longer needed. <br>
Risk: Generated market summaries or trading signals may be incomplete, stale, or unsuitable as financial advice. <br>
Mitigation: Treat outputs as informational market context and review them with appropriate financial judgment before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/avmw2025/crypto-market-intel) <br>
- [Market Data API Sources](artifact/references/api-sources.md) <br>
- [CoinGecko API Documentation](https://www.coingecko.com/en/api/documentation) <br>
- [Alternative.me Fear and Greed Index](https://alternative.me/crypto/fear-and-greed-index/) <br>
- [DeFi Llama API Documentation](https://defillama.com/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, json] <br>
**Output Format:** [JSON market-data files plus text or Markdown analysis prompts with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes crypto-latest.json and stocks-latest.json to the configured output directory; scripts can run on demand or through an optional cron schedule.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
