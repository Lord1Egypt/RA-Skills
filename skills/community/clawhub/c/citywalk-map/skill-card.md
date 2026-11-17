## Description:

Generates walking-route map HTML and optional PNG route cards from waypoint coordinates using OpenStreetMap tiles, OSRM routing, configurable theme colors, route statistics, and destination details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangfeng1995](https://clawhub.ai/user/huangfeng1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn city-walk waypoint lists into shareable walking-route maps for travel planning, itinerary summaries, and screenshot-ready route cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated maps can execute untrusted route titles, waypoint names, or descriptions as browser code.

Mitigation: Use only trusted route text and avoid opening or sharing generated maps built from untrusted route data.

Risk: The documented screenshot workflow can expose unrelated files if all of /tmp is served.

Mitigation: Serve only a dedicated localhost directory containing the generated map when taking screenshots.

Risk: Route coordinates and map views may be sent to external services including OSRM, tile providers, and optionally wttr.in or Nominatim.

Mitigation: Avoid processing sensitive locations and disclose external-service use before sharing or automating generated maps.

Risk: Optional rendering dependencies expand the local execution environment.

Mitigation: Install optional Python dependencies only in a controlled environment.

## Reference(s):

- [Citywalk Map on ClawHub](https://clawhub.ai/huangfeng1995/skills/citywalk-map)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [Leaflet.js](https://leafletjs.com/)
- [OSRM](https://project-osrm.org/)
- [Nominatim](https://nominatim.openstreetmap.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML or PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML defaults to /tmp/citywalk_map.html; optional PNG rendering requires Pillow and requests.]

## Skill Version(s):

2.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
