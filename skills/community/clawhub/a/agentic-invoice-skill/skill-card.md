## Description: <br>
Generate branded invoice and billing-document PDFs for agentic development services, including deposits, milestones, retainers, change orders, pass-through expenses, credits, receipts, refunds, and closeout billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[completetech](https://clawhub.ai/user/completetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and service teams use this skill to select invoice types and draft branded billing documents from verified contract, scope, milestone, payment, credit, refund, and support facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated invoices may contain incorrect invoice numbers, amounts, taxes, payment instructions, contract references, approval status, receipts, credits, refunds, or void notices. <br>
Mitigation: Review every generated billing artifact against the accounting source and verified contract or SOW facts before sending or relying on it. <br>
Risk: The skill can draft billing documents, but it does not execute payment operations or post to accounting ledgers. <br>
Mitigation: Keep payment collection, ledger posting, tax decisions, and collections workflows in the accounting system or under reviewer control. <br>
Risk: Draft invoice artifacts could be mistaken for final accounting records. <br>
Mitigation: Mark drafts clearly when payment details or tax handling are unknown and resolve TBD values before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/completetech/agentic-invoice-skill) <br>
- [Publisher profile](https://clawhub.ai/user/completetech) <br>
- [ClawHub metadata homepage](https://github.com/CompleteTech-LLC/agentic-invoice-skill) <br>
- [Invoice positioning](references/invoice-positioning.md) <br>
- [Invoice lifecycle](references/invoice-lifecycle.md) <br>
- [Invoice catalog](references/invoice-catalog.md) <br>
- [Use case decision table](references/use-case-decision-table.md) <br>
- [Template index](references/template-index.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown invoice drafts, branded PDF files, optional PNG previews, and local rendering commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated billing artifacts depend on user-provided invoice variables and must be checked against accounting sources before use.] <br>

## Skill Version(s): <br>
1.0.10 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
