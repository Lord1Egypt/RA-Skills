## Description: <br>
Provides Baidu Maps WebAPI guidance for building, reviewing, debugging, and directly calling map search, POI, routing, geocoding, traffic, administrative-region, weather, and pickup-point APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose Baidu Maps WebAPI endpoints, compose requests, handle API keys, and follow recipes for route planning, POI lookup, address conversion, weather lookup, and traffic-aware travel questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baidu Maps API keys can be exposed if copied into source code, chat logs, or shell history. <br>
Mitigation: Use BMAP_WEBAPI_AK from the environment or a server-side secret store, and avoid printing or committing the key. <br>
Risk: Map, routing, geocoding, and weather calls may send precise locations, home addresses, or travel intent to Baidu Maps. <br>
Mitigation: Send only the location data needed for the user-requested action, avoid unnecessary personal identifiers, and confirm before making external API calls with sensitive location data. <br>
Risk: Direct API calls can consume the user's Baidu Maps quota, and some advanced routing features require elevated permissions. <br>
Mitigation: Explain the endpoint and quota impact before live calls, use the standard endpoint for generated production code, and reserve the advanced experience endpoint for confirmed demonstrations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidu-maps/baidu-map-webapi) <br>
- [Baidu Maps Open Platform](https://lbs.baidu.com) <br>
- [Baidu Maps API key console](https://lbs.baidu.com/apiconsole/key) <br>
- [Skill guide](artifact/SKILL.md) <br>
- [Address or place name to POI recipe](artifact/recipes/address_to_poi.md) <br>
- [Route to named place recipe](artifact/recipes/route_to_named_place.md) <br>
- [Smart departure time recipe](artifact/recipes/smart_departure_time.md) <br>
- [Traffic-aware route recipe](artifact/recipes/traffic_aware_route.md) <br>
- [Weather query recipe](artifact/recipes/weather_query.md) <br>
- [Baidu Maps geocoding API reference](artifact/references/geocoding.md) <br>
- [Baidu Maps global reverse geocoding API reference](artifact/references/global_reverse_geocoding.md) <br>
- [Baidu Maps place search API reference](artifact/references/administrative_region_search.md) <br>
- [Baidu Maps place detail API reference](artifact/references/place_detail_search.md) <br>
- [Baidu Maps driving route API reference](artifact/references/driving_route_planning.md) <br>
- [Baidu Maps domestic weather API reference](artifact/references/domestic_weather_query.md) <br>
- [Baidu Maps overseas weather API reference](artifact/references/overseas_weather_query.md) <br>
- [Baidu Maps administrative division API reference](artifact/references/admin_division_query.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline curl commands, API request examples, and configuration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live API use requires curl and the BMAP_WEBAPI_AK environment variable.] <br>

## Skill Version(s): <br>
1.0.8 (source: evidence.release.version; artifact/SKILL.md frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
