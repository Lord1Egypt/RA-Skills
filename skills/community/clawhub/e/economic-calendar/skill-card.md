## Description: <br>
Fetches and displays filtered macroeconomic calendar events from Investing.com without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quantx-heiko](https://clawhub.ai/user/quantx-heiko) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts, traders, and workflow agents use this skill to retrieve macroeconomic events filtered by date range, country, importance, timezone, and language for briefings, scheduling, or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Economic event data is scraped from Investing.com and may be stale, incomplete, or affected by page and endpoint changes. <br>
Mitigation: Verify event times and values against another source before using the output for trading, scheduling, or other accuracy-sensitive decisions. <br>
Risk: Dependency versions are minimum-bounded rather than fully pinned. <br>
Mitigation: Install in a virtual environment and pin dependency versions before production use. <br>


## Reference(s): <br>
- [Country Codes Reference](references/country-codes.md) <br>
- [Investing.com Economic Calendar](https://www.investing.com/economic-calendar/) <br>
- [ClawHub Skill Page](https://clawhub.ai/quantx-heiko/economic-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Plain-text table to stdout, JSON to stdout, or JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports filters for date range, importance, countries, timezone, and language; requires network access to Investing.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
