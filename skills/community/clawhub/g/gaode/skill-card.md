## Description:

Gaode helps agents use Amap/Gaode Web Services for geocoding, POI search, routing, weather, IP location, and China coordinate-system guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Amap/Gaode mapping workflows such as address geocoding, reverse geocoding, POI search, route planning, weather lookup, IP location, and China coordinate-system conversion guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mapping queries may send addresses, coordinates, IP addresses, and arbitrary call parameters to Amap's external API.

Mitigation: Use the skill only with data appropriate for Amap Web Services and avoid sending sensitive location or personal data unless approved.

Risk: The CLI requires an AMAP_KEY and can make live network requests to restapi.amap.com.

Mitigation: Provide the key through environment configuration, restrict key permissions where possible, and review commands before execution.

## Reference(s):

- [Gaode ClawHub Skill Page](https://clawhub.ai/zhangifonly/skills/gaode)
- [Amap Web Service API Summary](https://lbs.amap.com/api/webservice/summary)
- [Amap REST API Endpoint](https://restapi.amap.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_KEY; live calls may send addresses, coordinates, IP addresses, and arbitrary call parameters to Amap Web Services.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
