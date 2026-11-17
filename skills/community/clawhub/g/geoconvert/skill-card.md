## Description:

Converts between street addresses and latitude/longitude coordinates using JisuAPI with Baidu or Google coordinate modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer address lookup, reverse geocoding, and map-coordinate questions by calling JisuAPI with a configured JISU_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Addresses, coordinates, and the API key are sent to JisuAPI for geocoding requests.

Mitigation: Use a dedicated JisuAPI key with quotas or restrictions, avoid sensitive home or work locations unless necessary, and rotate the key if request URLs or logs may have exposed it.

Risk: Geocoding results may be incomplete, imprecise, or unavailable for some inputs.

Mitigation: Review returned address details, precision, confidence, and error fields before relying on results for decisions or downstream location workflows.

## Reference(s):

- [JisuAPI GeoConvert API Documentation](https://www.jisuapi.com/api/geoconvert/)
- [JisuAPI](https://www.jisuapi.com/)
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/geoconvert)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and concise text guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, and JISU_API_KEY; sends address or coordinate queries to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
