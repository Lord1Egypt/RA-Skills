## Description:

Provides guidance for using Baidu Maps WebAPI to search places, resolve addresses and coordinates, plan routes, query traffic-aware travel times, inspect administrative regions, and retrieve weather information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to write, review, debug, or directly execute Baidu Maps WebAPI workflows for location search, geocoding, route planning, traffic-aware travel decisions, administrative-region lookup, and weather queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API calls can send addresses, coordinates, route details, vehicle identifiers, session identifiers, or free-form user requests to Baidu Maps.

Mitigation: Use the skill only for intended Baidu Maps WebAPI workflows, obtain appropriate user consent for sensitive location or vehicle data, and minimize data sent in each request.

Risk: Concrete API-key examples or request URLs may expose credentials or sensitive query details if copied into code or logs.

Mitigation: Replace examples with a restricted BMAP_WEBAPI_AK environment variable, avoid logging full request URLs, and rotate any credential that may have been exposed.

Risk: Advanced or experience endpoints may consume quota and may not be suitable for production workflows.

Mitigation: Prefer the standard Baidu Maps endpoint for production code and confirm with the user before direct calls that consume their access-key quota.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/skills/baidu-map-webapi)
- [Baidu Maps Open Platform](https://lbs.baidu.com)
- [Baidu Maps API Key Console](https://lbs.baidu.com/apiconsole/key)
- [百度地图全球逆地理编码 API](artifact/references/global_reverse_geocoding.md)
- [百度地图地理编码 API](artifact/references/geocoding.md)
- [百度地图地点检索及联想 API](artifact/references/administrative_region_search.md)
- [百度地图驾车路线规划 API](artifact/references/driving_route_planning.md)
- [百度地图步行路线规划 API](artifact/references/walking_route_planning.md)
- [百度地图骑行路线规划 API](artifact/references/cycling_route_planning.md)
- [百度地图公交路线规划 API](artifact/references/transit_route_planning.md)
- [百度地图国内天气查询 API](artifact/references/domestic_weather_query.md)
- [百度地图海外天气查询 API](artifact/references/overseas_weather_query.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with API parameters, curl examples, and integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a Baidu Maps WebAPI access key supplied through BMAP_WEBAPI_AK.]

## Skill Version(s):

1.0.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
