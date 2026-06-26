## Description: <br>
Generates isochrone maps by geocoding an address with Baidu, converting BD-09 coordinates to WGS84, calling the Mapbox Isochrone API, and producing shapefiles plus a preview image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggyybb](https://clawhub.ai/user/ggyybb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GIS analysts use this skill to turn a user-provided address, travel mode, and travel time into WGS84 isochrone artifacts for routing, accessibility, and map analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address inputs, derived coordinates, basemap imagery, previews, and shapefiles may be sent to external services including Baidu, Mapbox, ESRI, and Feishu. <br>
Mitigation: Use the skill only when this sharing is acceptable, and review organizational data-handling requirements before processing sensitive locations. <br>
Risk: The documented automatic Feishu delivery can share generated location artifacts without a clear confirmation step. <br>
Mitigation: Disable automatic sending or require manual confirmation of the Feishu destination before transmitting previews or ZIP archives. <br>
Risk: Baidu and Mapbox API keys are passed through runtime inputs and the skill documentation references loading them from memory. <br>
Mitigation: Provide keys through scoped secret storage, avoid broad memory exposure or shell history leakage, and rotate keys if they may have been exposed. <br>
Risk: The workflow depends on multiple geospatial Python packages and external APIs. <br>
Mitigation: Install dependencies in an isolated environment and pin or review packages before use in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ggyybb/baidu-mapbox-isochrone) <br>
- [Baidu Geocoding API endpoint](https://api.map.baidu.com/geocoding/v3/) <br>
- [Mapbox Isochrone API endpoint](https://api.mapbox.com/isochrone/v1/{profile}/{wgs_lng},{wgs_lat}) <br>
- [Mapbox Static Images API endpoint](https://api.mapbox.com/styles/v1/mapbox/streets-v12/static) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Shapefile components, GeoTIFF basemap, JPEG preview image, ZIP archive instructions, and status JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include WGS84 point and isochrone shapefiles, a WGS84 basemap GeoTIFF, a preview JPEG, and optional packaging for delivery.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
