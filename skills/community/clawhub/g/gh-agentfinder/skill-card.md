## Description:

Agentfinder helps agents search and compare skill candidates across named registries, request recommendations for a problem, and list available registries through a local API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Agentfinder to query a local skill-discovery API for search results, registry comparisons, and task-oriented recommendations. Results should be reviewed because the packaged implementation uses a small local index rather than a complete live registry search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and recommendation results may be incomplete or stale because the implementation uses a small packaged index.

Mitigation: Use results as candidates for human review and verify important skill choices against the source registry before adoption.

Risk: Problem descriptions submitted to the local recommendation endpoint may contain sensitive task details.

Mitigation: Run the service in an isolated Python environment and avoid submitting sensitive descriptions unless local processing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/gh-agentfinder)
- [Publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON API responses from local FastAPI endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and recommendation responses are bounded by request limits and draw from the packaged local index.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
