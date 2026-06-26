## Description: <br>
Provides AMap location services for route planning, POI search, geocoding, reverse geocoding, and static map generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttguy0707](https://clawhub.ai/user/ttguy0707) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query AMap for addresses, coordinates, routes, nearby places, and annotated static maps from an AMAP_API_KEY-enabled environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location requests can send addresses, coordinates, route endpoints, and POI search terms to AMap. <br>
Mitigation: Avoid submitting sensitive locations, review AMap data handling requirements, and use the skill only when sharing this location data with AMap is acceptable. <br>
Risk: The AMap API key may be exposed or misused if it is shared broadly or embedded into commands and logs. <br>
Mitigation: Use a dedicated API key where possible, keep it in AMAP_API_KEY, restrict its permissions or quota, and avoid pasting secrets into shared transcripts. <br>
Risk: Generated static map images may remain in local temporary storage after use. <br>
Mitigation: Delete generated map images when they are no longer needed, especially in shared or persistent workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttguy0707/amap-location) <br>
- [AMap REST API endpoint](https://restapi.amap.com/v3) <br>
- [AMap static map endpoint](https://restapi.amap.com/v3/staticmap) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash command examples; command output is text and generated static map image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY. Static map generation can write image files, with /tmp/static_map.png as the default output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
