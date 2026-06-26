## Description: <br>
Korean real-time air quality (PM10, PM2.5, O3, NO2, CO, SO2) and 1-3 day forecasts via Korea Environment Corporation AirKorea OpenAPI, with subcommands for station readings, province readings, forecasts, station lookup, TM coordinate lookup, and nearby station lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and automation agents use this skill to query Korean regulator-curated air-quality observations and forecasts for dashboards, alerts, school activity advisories, location-based AQI lookup, and research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a user-provided data.go.kr AirKorea API key to configured AirKorea endpoints. <br>
Mitigation: Use the default AirKorea endpoints unless an override is explicitly trusted, and keep the API key in the AIRKOREA_SERVICE_KEY environment variable. <br>
Risk: Some documented workflows can be adapted into shell command substitutions or eval-style patterns. <br>
Mitigation: Prefer the read-based examples and review shell pipelines before executing them with live credentials. <br>
Risk: AirKorea data is hourly, Korea-specific regulator data and is not personalized health advice. <br>
Mitigation: Use the output for Korean AQI lookup and operational alerts, and pair consumer-facing health recommendations with appropriate public-health guidance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/airkorea-cli) <br>
- [data.go.kr OpenData portal](https://www.data.go.kr/) <br>
- [AirKorea air-pollution information API](https://apis.data.go.kr/B552584/ArpltnInforInqireSvc) <br>
- [AirKorea measuring-station information API](https://apis.data.go.kr/B552584/MsrstnInfoInqireSvc) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with bash commands; runtime scripts emit JSONL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a user-provided AIRKOREA_SERVICE_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
