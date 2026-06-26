## Description: <br>
Citywalk Map generates customizable walking-route map outputs from waypoint coordinates using public map, routing, and optional weather services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn city walking itineraries into route-map artifacts with distance, timing, waypoint, theme-color, and optional weather context. It is suited for travel planning, route presentation, and local screenshot or image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route coordinates and generated screenshots can reveal sensitive location data. <br>
Mitigation: Avoid private home or work itineraries, review screenshot contents before sharing, and share generated map images only intentionally. <br>
Risk: The skill uses public mapping, routing, tile, and optional weather services that receive route coordinates or destination coordinates. <br>
Mitigation: Use the skill only when those services are acceptable for the itinerary, or configure trusted/self-hosted services where possible. <br>
Risk: Serving /tmp broadly for screenshots may expose unrelated local files. <br>
Mitigation: Serve only a dedicated output directory when using a local HTTP server for screenshot capture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangfeng1995/citywalk-map) <br>
- [OpenStreetMap](https://www.openstreetmap.org/) <br>
- [Leaflet.js](https://leafletjs.com/) <br>
- [OSRM](https://project-osrm.org/) <br>
- [Nominatim](https://nominatim.openstreetmap.org/) <br>
- [wttr.in](https://wttr.in/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated HTML and optional PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default HTML output is /tmp/citywalk_map.html; optional rendering can produce PNG route cards.] <br>

## Skill Version(s): <br>
2.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
