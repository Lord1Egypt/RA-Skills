## Description:

Unified GEO growth workflow for brand knowledge base building, LLM visibility audits, Doubao/DeepSeek readiness review, AI-GEO content asset generation, platform draft planning for Zhihu/Toutiao/CSDN/Juejin, client delivery reports, internal QA, and 7/14/30 day retests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, GEO delivery consultants, and content operators use this skill to turn brand materials into human-reviewed AI visibility audits, content gap analysis, platform draft plans, client delivery reports, internal QA reports, and retest plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports and local artifacts may contain sensitive brand or client materials.

Mitigation: For sensitive work, request summary-only output or use no-print script paths where available, then review generated files before sharing.

Risk: Drafts and recommendations could be mistaken for verified rankings, citations, traffic, or conversion outcomes.

Mitigation: Use the skill's evidence levels, require live or manual evidence for ranking and citation claims, and keep all platform drafts under human review.

Risk: The optional video workflow may run external npx/CDN dependencies.

Mitigation: Avoid that workflow unless dependencies are pinned or execution happens in a sandbox.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljseeking/skills/geo-growth-orchestrator)
- [Entity Evidence Rules](references/entity-evidence-rules.md)
- [GEO Unified Modules](references/geo-unified-modules.md)
- [Platform Style Guide](references/platform-style-guide.md)
- [GEO Orchestration Workflow](workflow/geo_orchestration_workflow.md)
- [Output Validation Rules](workflow/output_validation_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON artifacts, platform draft packets, retest plans, and optional shell commands for local report generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include local artifacts and full report text; platform drafts require human review before publishing.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
