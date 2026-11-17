## Description:

Searches public US legal opinions and browses court and judicial-person records through CourtListener via the Crawlora API, returning JSON research results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Legal researchers and developers use this skill to find public US opinion-search results, browse courts and judicial-person records, and assemble leads for review against primary legal sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and the Crawlora API key are sent to Crawlora.

Mitigation: Use a limited API key if available, avoid sensitive queries, and keep the key out of logs and shared shells.

Risk: Research results can be incomplete or unsuitable as authority for a legal conclusion.

Mitigation: Verify conclusions against primary opinions and the applicable jurisdiction.

## Reference(s):

- [CourtListener endpoint reference](reference/endpoints.md)
- [CourtListener Research on ClawHub](https://clawhub.ai/crawlora-org/skills/courtlistener-research)

## Skill Output:

**Output Type(s):** [Text, Research results]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public opinion-result, court, and judicial-person metadata; supports paginated searches and directory browsing.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
