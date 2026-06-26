## Description: <br>
A bidding-document domain knowledge skill that helps agents analyze tender requirements, prepare business, technical, and pricing sections, and check rejection risks and document consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bid and proposal teams use this skill as a structured bidding-document knowledge base for tender parsing, bid-section drafting, pricing tables, compliance checks, and consistency review. Without Universal Task OS available, it is limited to read-only reference lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to automatically install and use Universal Task OS for bidding workflows. <br>
Mitigation: Install only after reviewing the dependency behavior and confirming any dependency installation yourself. <br>
Risk: Bid documents may include confidential company, pricing, qualification, or tender information. <br>
Mitigation: Provide only necessary data, avoid unnecessary confidential material, and review generated content before submission. <br>
Risk: Incorrect, incomplete, or inconsistent bid content can create rejection or compliance risk. <br>
Mitigation: Use the skill's checks as assistance only and have qualified reviewers verify final bid documents against the tender requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/bidding-doc-domain) <br>
- [Bidding Catalog](references/bidding-catalog.md) <br>
- [Bidding Requirements](references/bidding-requirements.md) <br>
- [Exemplars](references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text, tables, checklists, document outlines, and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for missing bid facts, company details, pricing, schedule, warranty, or source tender text before producing bid-related outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
