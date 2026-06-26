## Description: <br>
专业财务报表审查 Skill，基于中国《会计法》《企业会计准则》和《税法》体系，对企业财务报表进行全面合规性审查、风险识别和分析，支持可扩展的策略库，包含税款比对分析、收入确认审查、成本操纵识别等多种专业策略，适用于年报审计、税务稽查准备、投资尽调、内部控制等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiliang911](https://clawhub.ai/user/weiliang911) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External finance, audit, tax, and due-diligence users can use this skill to parse financial statement files, run rule-based review strategies, identify accounting or tax risks, and produce review summaries for professional follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive financial files and can scan directories, which may expose confidential business or taxpayer data if used outside a controlled environment. <br>
Mitigation: Run it only in an approved secure environment, restrict input paths to the intended review set, and avoid broad directory scans unless access controls and data-handling procedures are in place. <br>
Risk: Document parsing dependencies and PDF handling can be risky when files are untrusted or dependencies are not pinned to reviewed versions. <br>
Mitigation: Pin and review parser dependencies, sandbox or resource-limit parsing execution, and avoid untrusted PDFs until those controls are applied. <br>
Risk: Generated accounting and tax findings may be incomplete, outdated, or unsuitable for a specific entity without professional judgment. <br>
Mitigation: Require review by qualified accounting or tax professionals before using outputs for audit, tax, investment, or management decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weiliang911/financial-statement-review) <br>
- [会计法及会计准则要点](references/accounting_law.md) <br>
- [中国税法要点摘要](references/tax_law_summary.md) <br>
- [财务报表审查方法论](references/review_methodology.md) <br>
- [策略开发指南](strategies/STRATEGY_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, CLI commands, and generated review report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk findings, estimated tax exposure, regulatory references, remediation suggestions, and saved report files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
