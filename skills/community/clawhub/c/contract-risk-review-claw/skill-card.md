## Description: <br>
合同风险审查虾帮助代理审查合同文本，识别不平等条款、违约责任失衡、知识产权、管辖权、模糊表述和隐藏义务等风险，并生成修订建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, procurement, operations, and business users can use this skill to review Chinese contract text, compare drafts against templates, and produce a structured risk report with suggested replacement language. It is intended to assist review, not replace professional legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract text may contain confidential or sensitive business information. <br>
Mitigation: Use the skill only with contracts the user is authorized to review and handle contract files according to the organization's confidentiality requirements. <br>
Risk: Generated legal analysis and replacement clauses may be incomplete or unsuitable for a specific jurisdiction or transaction. <br>
Mitigation: Treat outputs as review support and have qualified legal counsel validate high-risk findings and final contract language. <br>
Risk: Batch review or notification integrations could expose more documents or recipients than intended. <br>
Mitigation: Confirm scope, recipients, and permissions before batch-scanning repositories or connecting review findings to notification or compliance-monitoring workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/contract-risk-review-claw) <br>
- [Risk Clauses Reference](references/risk-clauses.md) <br>
- [Contract Templates Reference](references/contract-templates.md) <br>
- [Legal Regulations Reference](references/legal-regulations.md) <br>
- [Revision Suggestions Reference](references/revision-suggestions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown contract review report with risk summary, clause-level findings, revision suggestions, and replacement text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed by an authorized legal professional before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
