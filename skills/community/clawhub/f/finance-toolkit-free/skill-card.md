## Description: <br>
Provides delayed quotes and historical data for stocks, ETFs, indices, and foreign exchange, with local watchlist management and cache-aware lookup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal investors and agent users use this skill to look up market quotes, retrieve daily historical series, and maintain local watchlists for routine investment tracking and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests local file write and shell execution while the artifact includes only placeholder instructions and no referenced implementation files. <br>
Mitigation: Review the installed artifact before use, run it only in a constrained workspace, and verify any scripts or commands before execution. <br>
Risk: Portfolio or watchlist data could be exposed if callback_url is used without clear publisher documentation of what is sent and where. <br>
Mitigation: Do not use callback_url with personal financial data unless the publisher documents the destination and payload; keep callbacks disabled otherwise. <br>
Risk: Market data may be delayed or sourced from free or unofficial APIs, which can be unsuitable for trading or time-sensitive financial decisions. <br>
Mitigation: Use the output for routine tracking only and verify important decisions against an authoritative market-data source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/finance-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Project homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-shaped result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local watchlist or cache files when installed with write access; market data may be delayed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
