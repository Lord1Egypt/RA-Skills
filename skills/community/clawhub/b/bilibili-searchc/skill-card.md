## Description:

Real-time Bilibili video search that retrieves top video titles as structured JSON through a local API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raise7727](https://clawhub.ai/user/raise7727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search Bilibili for current videos by keyword and summarize or analyze the returned titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate local FastAPI service that controls browser automation.

Mitigation: Verify and run only the intended local service before enabling the skill, and keep the service bound to localhost.

Risk: Search keywords are sent to the local service for Bilibili searches.

Mitigation: Avoid sensitive search terms unless the local service and search workflow are acceptable for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raise7727/skills/bilibili-searchc)
- [OpenAPI Specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON search results with Bilibili video titles, suitable for downstream text analysis or summarization.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a keyword query and a separate localhost FastAPI service.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
