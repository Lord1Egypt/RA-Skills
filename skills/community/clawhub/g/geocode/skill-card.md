## Description:

Reverse geocode latitude and longitude coordinates to a human-readable region using geocode.com.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for low-frequency, interactive reverse geocoding when they need to turn decimal latitude and longitude into locality, region, and country text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can be redirected to arbitrary network endpoints through GEOCODE_BASE_URL, which may expose queried coordinates or route requests to an untrusted service.

Mitigation: Use the skill only with trusted HTTPS endpoints, keep GEOCODE_BASE_URL fixed in shared or automated environments, and avoid allowing untrusted prompts, users, or configuration to set it.

Risk: Reverse-geocoding sends latitude and longitude values to geocode.com.cn.

Mitigation: Use public endpoints only for low-frequency interactive lookups and only when sending the queried coordinates to the provider is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jvy/skills/geocode)
- [geocode.com.cn reverse-geocoding endpoint](https://geocode.com.cn/)
- [geocode.com.cn demo query](https://geocode.com.cn/?lat=39.9042&lon=116.4074)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and raw JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reverse-geocode responses are compact JSON arrays; the skill asks agents to summarize original coordinates, best available locality or region text, country or region, and any empty fields.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
