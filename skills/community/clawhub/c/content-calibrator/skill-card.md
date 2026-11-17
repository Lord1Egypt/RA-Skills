## Description:

Content Calibrator scores content across seven quality dimensions, predicts engagement, compares predictions with post-publication metrics, and evolves platform-specific rubrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to score drafts, predict engagement, review prediction accuracy after publication, and update rubrics by platform. It is intended for workflows where submitted content can be evaluated by external LLM services and retained in local calibration records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted drafts, customer material, or regulated content may be sent to external LLM services during scoring and prediction.

Mitigation: Use only with content that is approved for the configured LLM providers, and avoid confidential or regulated inputs unless the deployment's privacy requirements are satisfied.

Risk: Prediction and review workflows keep local calibration records, including content previews and actual performance metrics.

Mitigation: Review retention, access control, and deletion practices for data/content-calibrator before enabling the skill in sensitive workflows.

Risk: Rubric evolution can change platform-specific scoring weights based on historical review records.

Mitigation: Review generated rubric changes before relying on them for consequential content decisions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thcjp/skills/content-calibrator)
- [Business rules](references/business_rules.md)
- [Error codes](references/error_codes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses with scoring, prediction, review, and rubric-update data; Markdown examples document shell usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes prediction, review, and rubric records under data/content-calibrator when the corresponding actions run.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
