## Description: <br>
面向法律/财务/采购场景的合规审计引擎，自动提取风险条款、映射法规基线、生成审计底稿与澄清模板 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, finance, procurement, and internal-control teams use this skill to review contracts, tender documents, and internal policies against selected compliance scopes. It produces traceable risk mapping, audit workpaper drafts, clarification language, and remediation responsibility guidance for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The input materials may contain personal data, customer names, sensitive pricing, trade secrets, or regulated information. <br>
Mitigation: Redact sensitive business and personal information before use where possible. <br>
Risk: Generated compliance mappings, citations, and recommendations may be incomplete, outdated, or unsuitable for final decisions. <br>
Mitigation: Have qualified legal or compliance staff verify important citations, current-law status, and final decisions. <br>
Risk: The built-in knowledge base covers selected high-frequency regulations and may not cover every industry, local, or newly amended rule in the requested scope. <br>
Mitigation: Flag uncovered regulations for manual review and verify the current effective version of cited rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/boboy-j/compliance-audit-pro) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/boboy-j) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition and Knowledge Index](artifact/SKILL.md) <br>
- [Input Schema](artifact/schema.json) <br>
- [Usage Examples](artifact/examples.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown compliance audit report with risk tables, workpaper draft, clarification language, and remediation matrix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires document_content and compliance_scope inputs; supports an optional risk_threshold of low, medium, high, or strict.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
