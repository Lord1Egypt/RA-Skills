## Description:

Search for campgrounds, check availability and book campsites across the entire world.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsuppers](https://clawhub.ai/user/jsuppers)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search for campground, glamping, and RV site options, inspect listing details, check date-specific availability, and retrieve booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs the Campertunity MCP server through an unpinned npm package via npx.

Mitigation: Pin `campertunity-ai-tools` to a reviewed exact version where supported and run the MCP server with only the filesystem, environment-variable, and network access needed for campground search and booking-link workflows.

Risk: Availability is not supported for all campground listings.

Mitigation: When automated availability is unavailable, present the manual check or booking link clearly so users can verify dates before relying on the result.

## Reference(s):

- [Campertunity Homepage](https://campertunity.com)
- [ClawHub Skill Page](https://clawhub.ai/jsuppers/skills/campertunity)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown]

**Output Format:** [Markdown with JSON configuration and MCP tool workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include campground result tables with name, distance, rating, and price, plus booking URLs when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
