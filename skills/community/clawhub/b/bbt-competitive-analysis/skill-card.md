## Description:

Polls competitive crawl triggers, aggregates six months of product, review, and QA data by category, produces structured analysis context and a report skeleton, uploads outputs to OSS, and sends a DingTalk summary for scheduled competitor analysis in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wandervine](https://clawhub.ai/user/wandervine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run scheduled, database-driven competitor analysis in OpenClaw after crawl jobs complete. It standardizes category-level aggregation, report skeleton generation, OSS publication, and DingTalk notification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business analysis artifacts and analysis_context.json are uploaded to OSS using public-style URLs.

Mitigation: Use least-privilege OSS credentials, require HTTPS endpoints, keep buckets private, prefer signed expiring URLs, and review outputs for internal competitive intelligence before upload.

Risk: DingTalk summaries may expose report links or conclusions to a broad channel.

Mitigation: Use a narrow DingTalk recipient scope, configure webhook signing where available, and avoid posting to broad or unmanaged channels.

Risk: The workflow reads competitive-analysis tables and updates trigger consumption state.

Mitigation: Run only in a controlled enterprise environment with least-privilege database credentials and confirm the required trigger fields before scheduling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wandervine/skills/bbt-competitive-analysis)
- [Competitive Analysis Data Contract](references/data-contract.md)
- [OpenClaw Setup](references/openclaw-setup.md)
- [Competitive Analysis Report Outline](references/report-outline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON analysis context plus Markdown/HTML report skeletons, OSS manifest URLs, and a DingTalk markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads report.md, report.html, analysis_context.json, and a manifest to OSS; deeper narrative generation is left to the host runtime.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
