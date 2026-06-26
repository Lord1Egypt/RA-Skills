## Description: <br>
China Contract Review helps agents review Chinese contracts, identify legal and compliance risks, and suggest revisions for labor, sales, rental, service, cooperation, and confidentiality agreements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees can use this skill as a contract-review aid for Chinese-language agreements. It supports clause-by-clause review, risk identification, legal-reference prompts, revision suggestions, and structured review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract text may contain sensitive personal or business information. <br>
Mitigation: Process only contract content the user is allowed to share and avoid exposing confidential terms outside the intended agent workflow. <br>
Risk: The skill can produce legal-analysis text that may be incomplete, outdated, or inappropriate for a specific matter. <br>
Mitigation: Use the output as an informational review aid and have important contracts reviewed by a qualified legal professional. <br>
Risk: The optional python-docx dependency is not pinned in the artifact. <br>
Mitigation: Independently review or pin python-docx before installing it in controlled environments. <br>


## Reference(s): <br>
- [China Contract Review on ClawHub](https://clawhub.ai/tobewin/china-contract-review) <br>
- [tobewin publisher profile](https://clawhub.ai/user/tobewin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style contract review reports with risk summaries and suggested revisions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite Chinese legal provisions and should be treated as informational review support, not professional legal advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
