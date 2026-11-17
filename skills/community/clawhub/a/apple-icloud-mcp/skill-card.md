## Description:

Connects agents to Apple Music, iCloud Calendar, Contacts and Mail, Apple Maps, WeatherKit, podcasts, and iTunes/App Store search through Apple's web services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People use the skill to retrieve information from their Apple services and manage supported account data, such as playlists, calendar events, contacts, and email, through an agent on any operating system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the Apple connector for a request that does not specify Apple.

Mitigation: Use the connector when the user clearly asks for an Apple service; clarify the intended service when a generic request could match multiple connectors.

Risk: The scan had medium confidence and partial coverage because a local reference was unresolved, so not every referenced behavior was reviewed.

Mitigation: Review the skill and its referenced material before installation, especially before enabling account access or write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/apple-icloud-mcp)
- [npm package](https://www.npmjs.com/package/apple-icloud-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text and Markdown responses, with configuration examples when setup guidance is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on configured Apple service credentials and availability.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
