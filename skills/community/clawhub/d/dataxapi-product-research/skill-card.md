## Description:

Research TikTok Shop and Xiaohongshu products and reviews to summarize sales signals, buyer praise and complaints, and potential product gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Product researchers, sellers, and market analysts can use this skill to compare products and sampled customer reviews for a keyword on TikTok Shop or Xiaohongshu, then identify recurring praise, complaints, and possible product gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package is unpinned, so installation or execution could fetch a later version that was not reviewed.

Mitigation: Review and pin the CLI version used for a run, and reassess it when the version changes.

Risk: The security review is incomplete because some local path references could not be resolved.

Mitigation: Inspect unresolved package paths and review the full package before relying on it in a production workflow.

Risk: Product and review calls are pay per call and can incur charges.

Mitigation: Check the free plan's maximum cost and set a spend cap before running a query.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-product-research)

## Skill Output:

**Output Type(s):** [Analysis, Files, Markdown]

**Output Format:** [CSV product and review table with a Markdown product brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One review page per product is a sample; data fields not supplied by a platform may be empty.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
