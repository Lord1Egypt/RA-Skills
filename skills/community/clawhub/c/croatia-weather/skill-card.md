## Description:

Croatia Weather helps agents answer Croatia-focused and Europe-adjacent weather, forecast, warning, maritime, agriculture, hydrology, environment, and climate questions using official DHMZ public XML feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolicjakov](https://clawhub.ai/user/nikolicjakov)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and summarize official Croatian and European weather data for travel, safety checks, agriculture, maritime planning, hydrology, and climate comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to DHMZ-related public weather domains when invoked.

Mitigation: Review network policy before deployment and allow only the documented weather domains where outbound access is restricted.

Risk: Home-station environment variables can reveal a user's preferred or private location.

Mitigation: Use coarse station preferences when privacy matters and avoid exposing home-station settings in shared logs or transcripts.

Risk: Weather feeds, timestamps, and XML structures can change or return empty seasonal data.

Mitigation: Check the DHMZ feed reference and source timestamps before relying on outputs for safety-sensitive decisions.

## Reference(s):

- [DHMZ Quick Guide](references/quick-guide.md)
- [DHMZ Station Cross-Reference](references/stations.md)
- [DHMZ XML Feed Reference](https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici)
- [DHMZ](https://meteo.hr)
- [Open Licence of the Republic of Croatia](https://data.gov.hr/open-licence-republic-croatia)
- [Croatia Weather on ClawHub](https://clawhub.ai/nikolicjakov/skills/croatia-weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 stdlib command invocations; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
