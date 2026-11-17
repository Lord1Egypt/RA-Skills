## Description:

Find API helps agents identify reliable external data APIs across domains such as financial data, weather, news, maps, and e-commerce instead of defaulting to web scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesilsin-netizen](https://clawhub.ai/user/yesilsin-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when an agent needs to fetch external data and should choose reliable APIs before considering web scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broad API discovery guidance and package installation examples that may not be needed for every task.

Mitigation: Treat installation commands as optional, use a virtual environment, and install only packages required for the selected data source.

Risk: Some referenced APIs require API keys or account tokens.

Mitigation: Keep credentials out of chat, logs, notebooks, committed files, and shared outputs.

Risk: API recommendations, pricing, limits, and availability can change over time.

Mitigation: Confirm terms, quotas, and documentation with the chosen API provider before production use.

## Reference(s):

- [Find API ClawHub page](https://clawhub.ai/yesilsin-netizen/skills/find-api)
- [AKShare documentation](https://akshare.akfamily.xyz)
- [yfinance repository](https://github.com/ranaroussi/yfinance)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [NewsAPI](https://newsapi.org)
- [Amap API](https://lbs.amap.com)
- [RapidAPI Hub](https://rapidapi.com/hub)
- [Public APIs directory](https://github.com/public-apis/public-apis)
- [ProgrammableWeb](https://www.programmableweb.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with tables, links, shell commands, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API key setup guidance and package installation examples.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
