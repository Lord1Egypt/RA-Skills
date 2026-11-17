## Description:

Search web for user pain points and output a PRD JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Product builders, founders, and developers use this skill to search public web discussions for pain points and turn the results into a PRD-style JSON with user stories, MVP features, and OpenClaw tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to external search services.

Mitigation: Do not use confidential product names, customer data, secrets, or internal project details as keywords.

Risk: Baidu API key setup is documented, but the packaged script does not implement a Baidu network request.

Mitigation: Treat Baidu setup notes as inconsistent documentation and rely on Brave Search or Hacker News behavior unless the artifact is updated.

Risk: Generated PRD content depends on public search results and simple extraction logic.

Mitigation: Review source URLs, quotes, priorities, and generated tasks before using the output for product decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/skills/auto-prd-hunter)
- [Brave Search API](https://api.search.brave.com/)
- [Hacker News Algolia API](https://hn.algolia.com/api/v1/search)
- [Baidu Cloud](https://cloud.baidu.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success JSON with pain points, user stories, MVP features, OpenClaw tasks, source URLs, and generation metadata; returns error JSON when API searches fail or produce no results.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
