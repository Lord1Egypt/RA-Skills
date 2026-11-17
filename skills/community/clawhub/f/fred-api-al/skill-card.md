## Description:

Retrieve and cite U.S. and international economic time-series data such as GDP, inflation, unemployment, and interest rates from FRED.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer economic-data questions with the correct FRED series, units, date windows, and citations. It is suited for retrieving, comparing, transforming, and explaining historical macroeconomic time-series data while avoiding unsupported forecasts or market quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a FRED MCP server configured with a FRED API key, creating a secret-handling risk if the key is requested, logged, or echoed.

Mitigation: Keep the key in the server environment and follow the skill guidance to never request, reveal, log, or include it in output.

Risk: Economic answers can be misleading if an agent uses the wrong series, treats missing values as zero, reports an index as a rate, or ignores revisions.

Mitigation: Confirm series metadata, use FRED-provided transforms, handle missing values explicitly, and cite observation date, retrieval date, series ID, URL, and revision status.

Risk: FRED is not appropriate for real-time market quotes, company fundamentals, non-economic facts, or forecasts presented as data.

Mitigation: Route those requests to a more appropriate source and use FRED only for supported economic time-series data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simonpierreboucher02/skills/fred-api-al)
- [Official FRED API Documentation](https://fred.stlouisfed.org/docs/api/fred/)
- [FRED Endpoints and Tools](artifact/reference/endpoints.md)
- [FRED Series IDs, Units, and Frequency](artifact/reference/series-and-units.md)
- [FRED Response Fields](artifact/reference/response-fields.md)
- [FRED Common Errors](artifact/reference/common-errors.md)
- [FRED Best Practices](artifact/reference/best-practices.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown guidance with example JSON tool-call payloads and cited answer patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; expects a FRED MCP server configured with a FRED API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
