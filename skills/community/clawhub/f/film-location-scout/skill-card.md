## Description:

Discover nearby film and TV show shooting locations with cinematic scene recreation images, precise coordinates, scene descriptions, and weather-based photography parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kensonh](https://clawhub.ai/user/kensonh)

### License/Terms of Use:

MIT

## Use Case:

External users and travel photographers use this skill to find nearby film and TV locations, plan photo recreations, and receive location-specific shooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic IP-based location lookup and precise coordinates may reveal sensitive personal location details in chat output.

Mitigation: Use a coarse city or public landmark instead of a home or work address, and review generated location details before sharing logs.

Risk: The installer can update agent skill directories across multiple platforms.

Mitigation: Run the installer only for the platform you intend to update, and use dry-run mode before installation when reviewing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kensonh/skills/film-location-scout)
- [Scene prompt templates](artifact/scene-prompts.md)
- [Photography parameters reference](artifact/photo-params-reference.md)
- [IP geolocation endpoint](https://ipinfo.io/json)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Image prompts, Configuration]

**Output Format:** [Markdown cards with location details, camera settings, map links, and image generation outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five self-contained location cases with film information, GPS coordinates, photography parameters, and scene recreation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
