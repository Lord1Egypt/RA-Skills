## Description: <br>
面向上市公司财务部门的发票识别与自动入账技能，通过 OCR 从拍照或截图中提取发票数据，并支持验真、分类、三单匹配和台账管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aolikeji](https://clawhub.ai/user/aolikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance employees use this skill to extract invoice fields from images, verify invoice status, classify purchase and sales invoices, prepare accounting entries, and maintain invoice ledgers. It is intended for invoice-specific finance workflows that remain subject to finance staff confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive business invoice data. <br>
Mitigation: Restrict activation to invoice-specific requests, limit access to authorized finance users, and avoid unnecessary retention or sharing of invoice images and extracted fields. <br>
Risk: External tax verification may disclose invoice details or rely on external availability and policy constraints. <br>
Mitigation: Require explicit user or finance-admin confirmation before external verification and treat verification results as advisory until reviewed by finance staff. <br>
Risk: Automatic ledger or accounting writes could create incorrect records if OCR, matching, or classification is wrong. <br>
Mitigation: Require human approval before posting ledger updates, preserve reviewable source fields, and route low-confidence or mismatched invoices to manual review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aolikeji/skills/finance-invoice-ocr) <br>
- [ClawHub metadata homepage](https://clawhub.ai/skills/finance-invoice-ocr) <br>
- [National VAT invoice verification platform](https://inv-veri.chinatax.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured tables, formulas, workflow steps, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted invoice fields, verification status, accounting-entry suggestions, ledger schemas, and human-confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
