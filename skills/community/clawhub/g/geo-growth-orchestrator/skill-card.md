## Description: <br>
Unified GEO growth workflow for brand knowledge base building, LLM visibility audits, Doubao/DeepSeek readiness review, AI-GEO content asset generation, platform draft planning for Zhihu/Toutiao/CSDN/Juejin, client delivery reports, internal QA, and 7/14/30 day retests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, content operators, and GEO service consultants use this skill to turn brand materials into human-reviewed AI visibility audits, content gap analysis, platform draft plans, delivery reports, and retest plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may process sensitive business materials and generate local Markdown or JSON artifacts. <br>
Mitigation: Use only appropriate brand materials, keep generated artifacts in approved workspaces, and review outputs before sharing. <br>
Risk: Live probing may require credentials or API keys if the user intentionally enables it. <br>
Mitigation: Do not provide API keys unless live checks are required, and keep all credential handling under the user's normal security controls. <br>
Risk: Generated platform drafts or GEO recommendations may contain unsupported claims if source materials are incomplete. <br>
Mitigation: Manually review every draft, confirm facts and compliance boundaries, and avoid auto-publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ljseeking/geo-growth-orchestrator) <br>
- [Entity Evidence Rules](artifact/references/entity-evidence-rules.md) <br>
- [Unified GEO Modules](artifact/references/geo-unified-modules.md) <br>
- [Platform Style Guide](artifact/references/platform-style-guide.md) <br>
- [GEO Orchestration Workflow](artifact/workflow/geo_orchestration_workflow.md) <br>
- [Output Validation Rules](artifact/workflow/output_validation_rules.md) <br>
- [Platform Routing Rules](artifact/workflow/platform_routing_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON artifacts, content drafts, action plans, and optional shell commands for local report generation or validation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed GEO delivery packages and may save local Markdown/JSON artifacts when run in a workspace.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
