## Description: <br>
Track stocks, ETFs, indices, crypto (where available), and FX pairs with caching and provider fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anton-roos](https://clawhub.ai/user/anton-roos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch market quotes, generate stock or ETF price series, and maintain a local watchlist for concise finance summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs finance-data dependencies and runs Python scripts. <br>
Mitigation: Use a dedicated virtual environment and review or pin dependency versions when reproducibility matters. <br>
Risk: The skill contacts public market-data APIs that may be delayed, rate-limited, or unavailable. <br>
Mitigation: Preserve source and timestamp details in summaries, use the built-in cache and throttling behavior, and avoid presenting provider data as guaranteed real-time. <br>
Risk: The skill creates local cache and watchlist files. <br>
Mitigation: Run it in an appropriate workspace and review or remove local cache state when it is no longer needed. <br>


## Reference(s): <br>
- [Provider notes](artifact/providers.md) <br>
- [ExchangeRate-API Open Access endpoint](https://open.er-api.com/v6/latest/<BASE>) <br>
- [ClawHub skill page](https://clawhub.ai/anton-roos/finance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands, JSON command output, and CSV series output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cache and watchlist files while retrieving public market data from configured providers.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
