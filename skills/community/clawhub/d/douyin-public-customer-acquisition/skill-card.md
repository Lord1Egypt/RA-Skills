## Description:

Searches public Douyin videos, creator profiles, comments, and trending lists, returning structured data for content, competitor, sentiment, and lead analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, growth, marketing, and content teams can use this skill to inspect public Douyin content and comments, identify trends and competitor patterns, and organize demand or lead signals for authorized internal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that supplied links or IDs may be transmitted to a third-party service, and scanner coverage was partial.

Mitigation: Review the service and data handling before use; submit only public, non-sensitive links or IDs and protect the required API token.

Risk: Comment and creator data could expose personal identifiers or be used for unsolicited outreach or redistribution.

Mitigation: Keep results to authorized internal analysis, remove user IDs before sharing, and do not use the data for harassment or resale.

## Reference(s):

- [Douyin data service](https://www.guaikei.com)
- [Customer acquisition guide](artifact/references/customer-acquisition.md)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Usage and command options](artifact/references/options.md)
- [Error handling guide](artifact/references/errors.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance, Shell commands]

**Output Format:** [Structured JSON results and concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin data only; results can include content metadata, creator information, engagement counts, comments, and trend data.]

## Skill Version(s):

1.5.2 (source: server-resolved release metadata, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
