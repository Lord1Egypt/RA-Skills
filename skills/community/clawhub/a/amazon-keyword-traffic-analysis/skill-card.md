## Description:

Analyze Amazon keyword demand, market structure, weekly trends, observed SERP signals, and ASIN keyword visibility or traffic observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, analysts, and agent operators use this skill to investigate Amazon keyword demand, market structure, traffic-term discovery, and evidence-bounded ASIN keyword or traffic diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ZooData requests may consume credits and send requested keywords, ASINs, dates, marketplaces, public page URLs, and optional seller exports to ZooData.

Mitigation: Use the skill only with a ZooData account approved for this work, review requested inputs before execution, and provide SQP or Ads exports only when seller-funnel or advertising analysis is required.

Risk: The skill produces evidence-bounded traffic and keyword analysis, not direct bid, budget, pause, or negative-keyword decisions.

Mitigation: Treat outputs as validation priorities and require seller ABA-SQP or Amazon Ads data before operational advertising decisions.

Risk: A valid ZOODATA_API_KEY is required for normal operation.

Mitigation: Provide the key through the declared environment variable, limit access to authorized operators, and rotate or revoke credentials according to the publisher's credential policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apiclaw/skills/amazon-keyword-traffic-analysis)
- [Publisher profile](https://clawhub.ai/user/apiclaw)
- [Metadata homepage](https://github.com/SerendipityOneInc/ZooData-Skills)
- [README](README.md)
- [Production API and acquisition-surface contract](references/reference.md)
- [Execution guide](references/execution-guide.md)
- [Evidence protocols](references/evidence-protocols.md)
- [Output rules](references/output-rules.md)
- [SQP field semantics](references/sqp-field-semantics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with evidence-bounded analysis and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY; ZooData API calls may consume credits.]

## Skill Version(s):

0.1.6 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
