## Description:

Searches Douyin public content, creator posts, comments, individual post details, and trending topics for social media research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, marketers, and analysts use this skill to research public Douyin videos, creator activity, comments, and trends for topic discovery, competitor monitoring, and audience research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill benign with medium confidence and reports that some source files were not fully inspected.

Mitigation: Review the package contents before installation and keep the API token private.

Risk: The scan notes an individual post-detail lookup beyond the stated capability list.

Mitigation: Confirm that retrieving individual post details fits the intended use.

Risk: Search terms and Douyin links are sent to Guaikei's third-party API.

Mitigation: Use public content and send only queries or links you are authorized to share with that service.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-search-guaikei)
- [Guaikei service and access](https://www.guaikei.com)
- [Parameter options](references/options.md)
- [Comment demand mining guide](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelopes with search, creator, comment, post detail, and trending data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media links may expire; result limits depend on the API plan.]

## Skill Version(s):

1.4.2 (source: release evidence, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
