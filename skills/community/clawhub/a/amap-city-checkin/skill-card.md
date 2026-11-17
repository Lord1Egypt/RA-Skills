## Description:

Generates an Amap city check-in list and map QR code from a city name by searching popular attractions, cafes, bookstores, landmarks, and other places, then organizing results by category and district.

This skill is ready for commercial/non-commercial use.

## Publisher:

[770600682-cyber](https://clawhub.ai/user/770600682-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to turn a city, theme, or district request into a categorized check-in itinerary with Amap points of interest and a shareable map QR code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends city, district, and place-search queries to Amap.

Mitigation: Use the skill only when sharing those travel-planning queries with Amap is acceptable.

Risk: The skill requires an Amap API key.

Mitigation: Store AMAP_API_KEY as an environment variable and avoid placing it in prompts, logs, or shared files.

Risk: Ambiguous prompts could invoke the skill unintentionally.

Mitigation: Ask the user to confirm that they want a check-in map or list before using the skill on ambiguous travel prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/770600682-cyber/skills/amap-city-checkin)
- [Amap Open Platform](https://lbs.amap.com)
- [Amap Web Service API documentation](https://lbs.amap.com/api/webservice/summary)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown itinerary with categorized place lists, route suggestions, and a map QR code reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY and sends city, district, and place-search queries to Amap.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
