## Description:

Searches Bilibili by keyword through a companion local service and returns current video search results for agent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raise7727](https://clawhub.ai/user/raise7727)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to search Bilibili by keyword and retrieve current video results for trend tracking, creator monitoring, and competitive research. Use requires an intentionally trusted local service on 127.0.0.1:8000.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards user-provided keywords to a trusted local service, which may browse Bilibili or log requests depending on that service's implementation.

Mitigation: Install and use only when intentionally running and trusting the companion FastAPI service on 127.0.0.1:8000; avoid sensitive search keywords.

Risk: The skill depends on the companion local FastAPI and Playwright/Chromium setup being available and correctly configured.

Mitigation: Start the expected local service and verify its browser automation dependencies before relying on search results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raise7727/skills/bilibili-search-raise7727)
- [Publisher profile](https://clawhub.ai/user/raise7727)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text response, typically JSON-formatted search results from the local service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the local service response for the supplied keyword; no additional post-processing is evidenced.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
