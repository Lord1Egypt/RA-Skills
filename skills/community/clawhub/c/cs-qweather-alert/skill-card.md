## Description:

Provides QWeather-powered current weather, daily forecasts, and active weather alerts for a requested city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[savior1987](https://clawhub.ai/user/savior1987)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer city weather questions, including current conditions, 3-30 day forecasts, and active weather alert details from QWeather.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QWeather API credentials could leak if unsafe hosts or overly broad account privileges are used.

Mitigation: Use only a trusted HTTPS QWeather API host, keep the JWT least-privileged, and prefer passing credentials explicitly for sensitive deployments.

Risk: A shared ~/.openclaw/.env file or default token file can expose credentials to other local workflows.

Mitigation: Avoid relying on shared credential files on multi-user systems and restrict file permissions for any stored tokens.

Risk: City lookup history and operational details can persist in scripts/data/location.json and /tmp/cslog.

Mitigation: Periodically delete the cache and log directory when location-query history is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/savior1987/skills/cs-qweather-alert)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text weather reports with command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a QWeather API host and JWT token; may update scripts/data/location.json and write logs under /tmp/cslog.]

## Skill Version(s):

2.0.0 (source: server release evidence and target metadata; artifact _meta.json lists 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
