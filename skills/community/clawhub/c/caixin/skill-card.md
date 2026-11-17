## Description:

Retrieves and summarizes public news and trending topics from Caixin's open channels using keyword search, channel stats, and topic collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to summarize public Caixin news search results, channel hot items, and topic article collections without accessing paid or login-only content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misused to request paid, login-only, or otherwise restricted Caixin content.

Mitigation: Use it only for publicly available Caixin pages and do not attempt paywall, login, or access-control circumvention.

Risk: Broad trigger wording may lead to overly broad collection or irrelevant automation.

Mitigation: Keep requests narrow, avoid batch scraping, and follow Caixin platform rules and rate expectations.

Risk: Dynamic pages may produce incomplete or stale summaries if collected before content finishes loading.

Mitigation: Wait for page loading before summarizing and include source links and collection time in results.

## Reference(s):

- [Caixin homepage](https://www.caixin.com/)
- [ClawHub skill page](https://clawhub.ai/codenova58/skills/caixin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and structured text lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should include source links and collection time when available.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
