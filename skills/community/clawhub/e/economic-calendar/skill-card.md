## Description:

Fetches and filters macro-economic calendar events from Investing.com without an API key, with table and JSON output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantx-heiko](https://clawhub.ai/user/quantx-heiko)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to retrieve filtered economic calendar events for briefings, dashboards, automation, or market-monitoring workflows. It supports date ranges, importance levels, country filters, timezone selection, language selection, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Investing.com and depends on network access and the site's calendar response format.

Mitigation: Run it in an isolated Python environment where outbound requests to Investing.com are expected, and verify source availability before relying on results.

Risk: Unpinned dependencies and the documented lxml dependency can affect reproducibility.

Mitigation: Pin dependencies for production use and add lxml to the installation requirements before deployment.

Risk: Timezone conversion may be inaccurate if event source assumptions or daylight-saving behavior differ from the script's conversion logic.

Mitigation: Verify timezone conversion against a trusted calendar source before relying on event times.

Risk: The default JSON mode writes calendar files in the current working directory.

Mitigation: Use stdout or none for JSON mode when file creation is not desired, or run the skill in a directory where calendar output files are expected.

## Reference(s):

- [Economic Calendar ClawHub Page](https://clawhub.ai/quantx-heiko/skills/economic-calendar)
- [Country Codes Reference](artifact/references/country-codes.md)
- [Investing.com Economic Calendar](https://www.investing.com/economic-calendar/)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [Terminal table text or structured JSON calendar data, with optional calendar_YYYYMMDD.json files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include event date, time, currency, importance, event name, actual, forecast, and previous values.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
