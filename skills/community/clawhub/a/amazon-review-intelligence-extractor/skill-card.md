## Description:

Extracts consumer insights from Amazon reviews across 11 dimensions, compares competitor sentiment, and generates listing copy suggestions using ZooData API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and ecommerce operators use this skill to turn Amazon ASIN or category review data into pain-point, buying-factor, user-profile, competitor-comparison, and listing-copy guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a ZooData API bearer key and may make paid API calls.

Mitigation: Set the key only in the environment, prefer a scoped or low-credit key, and confirm expected credit use before broad or multi-call scans.

Risk: Fallback analysis can be influenced by untrusted raw review text.

Mitigation: Treat fallback results as directional, preserve data-provenance notes, and review generated conclusions before relying on them for business decisions.

Risk: Unpinned install commands may resolve different package contents over time.

Mitigation: Review and scan the resolved release artifact before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apiclaw/skills/amazon-review-intelligence-extractor)
- [Publisher profile](https://clawhub.ai/user/apiclaw)
- [ZooData Skills repository](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData API key setup](https://zoodata.ai/en/api-keys)
- [ZooData pricing](https://zoodata.ai/en/pricing)
- [ZooData API field reference](references/reference.md)
- [ZooData CLI contract](references/cli-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with structured sections and optional JSON evidence from ZooData CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY; API calls consume ZooData credits; fallback analysis may use raw Amazon review text.]

## Skill Version(s):

1.0.9 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
