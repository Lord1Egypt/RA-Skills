## Description: <br>
Uses AKShare to answer Chinese market-data questions about A-shares, China indexes, open-end mutual funds, macro indicators, macro calendar events, and finance news flashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickdeep1234](https://clawhub.ai/user/nickdeep1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to map Chinese market-data questions to a fixed AKShare-backed CLI and return concise Chinese summaries for stocks, indexes, funds, macro series, calendars, and finance news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data can be ambiguous, unavailable, delayed, or truncated depending on the AKShare dataset and symbol resolution. <br>
Mitigation: Use the bundled resolver behavior, surface ambiguous candidates instead of guessing, and summarize the returned rows with dataset and date context. <br>
Risk: The skill executes local Python commands and depends on the user's environment having the required dependencies. <br>
Mitigation: Run only the bundled query_akshare.py command path and relay missing-dependency guidance from the script error payload. <br>


## Reference(s): <br>
- [AKShare documentation](https://akshare.akfamily.xyz/data/index.html) <br>
- [AKShare Dataset Mapping](artifact/references/datasets.md) <br>
- [ClawHub skill page](https://clawhub.ai/nickdeep1234/ashare) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Chinese Markdown summary plus JSON data returned by the bundled CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are limited to the bundled Python script and whitelisted AKShare datasets.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
