## Description: <br>
Poll competitive crawl triggers, aggregate the last 6 months of product, review, and QA data by category, produce structured analysis context and a report skeleton, upload outputs to OSS, then send a DingTalk summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wandervine](https://clawhub.ai/user/wandervine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run scheduled, database-driven competitor analysis in OpenClaw after crawl jobs complete. It consumes successful trigger rows, aggregates product, review, and QA data by category, generates structured analysis context plus report skeletons, uploads outputs to OSS, and sends DingTalk summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads competitive-analysis database tables and updates trigger consumption fields. <br>
Mitigation: Use least-privilege database credentials with read access to analysis tables and update access limited to the trigger consumption fields. <br>
Risk: Generated reports and analysis_context.json may contain business-sensitive competitive data and are uploaded to OSS. <br>
Mitigation: Use a dedicated bucket or prefix, verify OSS destination and access policy, and review generated outputs before scheduling against production data. <br>
Risk: DingTalk summaries are sent through a configured webhook. <br>
Mitigation: Use an approved DingTalk robot, store webhook secrets through the host environment, and rotate credentials if a webhook is exposed. <br>
Risk: Some business metrics, including price, sales revenue, target age, and explicit positioning, may be unavailable in the current schema. <br>
Mitigation: Treat placeholders and heuristic fields as analysis gaps, not final facts, and enrich source tables before making pricing or launch decisions. <br>


## Reference(s): <br>
- [Competitive Analysis Data Contract](references/data-contract.md) <br>
- [OpenClaw Setup](references/openclaw-setup.md) <br>
- [Competitive Analysis Report Outline](references/report-outline.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wandervine/bbt-competitive-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON analysis context, Markdown and HTML report skeletons, OSS manifest URLs, and DingTalk markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PostgreSQL, Alibaba Cloud OSS credentials, DingTalk webhook configuration, and Python runtime dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
