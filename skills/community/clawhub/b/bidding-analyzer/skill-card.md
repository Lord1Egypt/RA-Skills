## Description: <br>
Analyzes bidding documents and company knowledge base content to produce bid preparation checklists, requirement response drafts, risk notes, scoring simulations, win probability estimates, and competitive strategy reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External bid teams, sales engineers, and proposal managers use this skill to analyze tender documents against company knowledge bases, draft bid response material, surface bid risks, simulate scoring, and shape competitive strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive bid, pricing, customer, and competitor information. <br>
Mitigation: Use excerpts or pre-filtered RAG snippets where possible, and redact personal data, secrets, proprietary pricing, customer-confidential material, and trade secrets before use. <br>
Risk: Scoring, win-probability, risk, and strategy outputs may affect business-critical bidding decisions. <br>
Mitigation: Have a responsible bid owner review generated scoring, win-probability, risk, and strategy content before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/bidding-analyzer) <br>
- [README](artifact/README.md) <br>
- [Input schema](artifact/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce long, budget-scaled reports with bid checklists, response matrices, risk tables, scoring estimates, and strategy recommendations.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
