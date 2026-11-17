## Description:

技术领域竞争格局分析，包含玩家分层、技术路线差异化与空白机会识别。当用户请求玩家图谱绘制、行业竞争对手分析、技术路线玩家对比、国内外玩家对比，或在特定技术领域内开展多玩家竞争评估时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and strategy teams use this Chinese-language skill to produce evidence-driven competitive landscape reports for a technology sector or track. It supports player discovery, competitor tiering, technology-route comparison, top-player profiles, and whitespace opportunity analysis for strategic planning, market-entry, investment screening, or R&D direction setting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates local evidence and report files during a run.

Mitigation: Run it in a dedicated project folder and review changed files before sharing or committing outputs.

Risk: Competitive landscape claims can be incomplete when structured patent, paper, or search tools are unavailable or degraded.

Mitigation: Require source_index.csv and claim_ledger.csv support for major claims, and clearly label degraded coverage in method_decisions.md and the final report.

Risk: Optional docx or pdf export depends on external rendering tools that may not exist in every runtime.

Mitigation: Treat Markdown plus evidence files as the default deliverable and confirm export tooling before promising docx or pdf outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/competitive-landscape-zhcn)
- [Workflow](references/workflow.md)
- [Source Routing](references/source-routing.md)
- [Quality Gates](references/quality-gates.md)
- [Evidence Schema](references/evidence-schema.md)
- [Method Benchmark](references/method-benchmark.md)
- [Domain Playbooks](references/domain-playbooks.md)
- [Deliverables](references/deliverables.md)

## Skill Output:

**Output Type(s):** [markdown, text, guidance, configuration]

**Output Format:** [Structured Markdown report with supporting CSV evidence files; optional docx or pdf export when suitable tooling is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local request, workplan, method decision, query log, source index, claim ledger, and report files in the run folder.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
