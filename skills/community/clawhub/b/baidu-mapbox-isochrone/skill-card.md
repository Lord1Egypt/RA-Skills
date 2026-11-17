## Description:

Generates isochrone maps by geocoding an address with Baidu, converting BD-09 coordinates to WGS84, calling the Mapbox Isochrone API, and producing shapefiles plus a preview image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggyybb](https://clawhub.ai/user/ggyybb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GIS users use this skill to generate travel-time isochrone shapefiles and preview maps from a named address, travel mode, and duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise addresses, coordinates, shapefiles, imagery, and preview images may be sent to Baidu, Mapbox, ESRI, and a Feishu destination.

Mitigation: Require explicit user approval before external API calls and before any message or file send; confirm the recipient and destination channel.

Risk: API keys are described as coming from memory and may be passed on the command line.

Mitigation: Use scoped environment variables or a secret manager for Baidu and Mapbox credentials, and avoid exposing secrets in shell history or process arguments.

Risk: The skill depends on several Python packages and geospatial libraries that may vary by environment.

Mitigation: Install dependencies in a pinned virtual environment before use and review the generated artifacts before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ggyybb/skills/baidu-mapbox-isochrone)
- [Baidu Geocoding API endpoint](https://api.map.baidu.com/geocoding/v3/)
- [Mapbox Isochrone API endpoint](https://api.mapbox.com/isochrone/v1/{profile}/{wgs_lng},{wgs_lat})
- [Mapbox Static Images API endpoint](https://api.mapbox.com/styles/v1/mapbox/streets-v12/static)
- [ArcGIS World Imagery tile service](https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{ty}/{tx})

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated GIS/image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates WGS84 point and isochrone shapefiles, a WGS84 GeoTIFF basemap, a JPG preview, and a ZIP package when the sending workflow is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
