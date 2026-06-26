## Description: <br>
Contract Auditor reviews Chinese contract text from Word or text inputs, identifies payment, delivery, compliance, and clause-risk issues, and produces audit findings with suggested revisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjmfjoy](https://clawhub.ai/user/bjmfjoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, legal, and project teams use this skill to perform an initial review of Chinese service or procurement contracts, summarize risk level, and locate clauses that may need revision. It is intended as a review aid and not as a substitute for legal counsel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated review may miss issues or provide misleading legal guidance. <br>
Mitigation: Treat the audit output as an aid and have important contracts reviewed by qualified legal staff. <br>
Risk: Word annotation writes an output file and may affect the working copy if the path is chosen poorly. <br>
Mitigation: Run the skill on copies of important contracts and confirm the annotated output path before execution. <br>
Risk: Unpinned dependencies can change behavior across environments. <br>
Mitigation: Pin and review dependencies in controlled environments before operational use. <br>


## Reference(s): <br>
- [Contract Auditor on ClawHub](https://clawhub.ai/bjmfjoy/contract-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/bjmfjoy) <br>
- [Design document](docs/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit reports, annotated Markdown contracts, and optionally annotated Word documents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include risk level, issue counts, categorized findings, issue descriptions, and suggested revisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
