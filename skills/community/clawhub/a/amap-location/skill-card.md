## Description:

高德地图服务（路径规划、POI 搜索）

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttguy0707](https://clawhub.ai/user/ttguy0707)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call AMap services for geocoding, reverse geocoding, driving, walking, transit route planning, POI search, and static map generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, coordinates, route endpoints, and the AMap API key are sent to AMap.

Mitigation: Use the skill only when this data sharing is acceptable; protect, restrict, and rotate the AMap API key.

Risk: Static map generation can create an image file containing location context.

Mitigation: Store generated map images only where appropriate and delete temporary files when they are no longer needed.

Risk: Transit routing defaults to Guangzhou and the interface is Chinese-only.

Mitigation: Confirm the city and language fit the deployment context before relying on transit results.

Risk: The artifact prompts installation of Pillow without a pinned package version.

Mitigation: Install Pillow from a pinned or trusted dependency source.

## Reference(s):

- [AMap REST API v3 endpoint](https://restapi.amap.com/v3)
- [AMap static map endpoint](https://restapi.amap.com/v3/staticmap)
- [ClawHub skill page](https://clawhub.ai/ttguy0707/skills/amap-location)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Plain text and Markdown with shell command examples; static map output is a PNG file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_API_KEY environment variable and may write a temporary static map image.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
