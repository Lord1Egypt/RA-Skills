## Description:

零配置即装即用，一键唤起高德地图APP打车，另含驾车/公交/步行/骑行路线规划、IP定位、周边搜索、POI搜索，免申请Key即用。暑期出行打车、目的地接送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for Gaode Maps taxi launch links, route planning, IP location, and POI search results for travel and local navigation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Addresses, coordinates, POI searches, route requests, and possible IP-location requests are sent to an external Gaode proxy.

Mitigation: Review privacy handling before installation, disclose this data flow to users, and avoid sending sensitive location queries unless necessary.

Risk: The artifact uses an embedded shared proxy token that should be treated as exposed.

Mitigation: Remove the shared token and require a user-controlled secret or trusted deployment configuration before production use.

Risk: The documented primary environment variable differs from the proxy token environment variable used by the helper script.

Mitigation: Align the environment variable names or clearly document the required variables before relying on token override behavior.

Risk: The helper exposes more map functions than the public description highlights.

Mitigation: Inventory and allowlist only the map functions needed for the deployment, and document the enabled functions for reviewers and users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/gaode-taxi)
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON responses and generated Gaode Maps app URI strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return taxi launch links, route details, location lookup results, POI search results, weather data, distance measurements, static map URLs, or error messages.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
