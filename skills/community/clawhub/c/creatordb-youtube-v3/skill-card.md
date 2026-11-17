## Description:

Searches CreatorDB for YouTube creators and retrieves channel profile, performance, content, sponsorship, and audience information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poi5305](https://clawhub.ai/user/poi5305)

### License/Terms of Use:


## Use Case:

Developers, analysts, and creator-marketing teams use this skill to query CreatorDB for YouTube creator discovery and channel analytics when they have a CreatorDB API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator searches and channel IDs are sent to CreatorDB using the user's CreatorDB API key.

Mitigation: Use the skill only for workflows where sending those queries to CreatorDB is expected and approved.

Risk: Audience and sponsorship analytics are third-party data and may not be appropriate for sensitive or confidential targets.

Mitigation: Review returned analytics before relying on them and avoid querying sensitive targets unless that fits the workflow.

## Reference(s):

- [CreatorDB](https://www.creatordb.app)
- [ClawHub skill page](https://clawhub.ai/poi5305/skills/creatordb-youtube-v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and CREATORDB_API_KEY; API responses are third-party CreatorDB data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
