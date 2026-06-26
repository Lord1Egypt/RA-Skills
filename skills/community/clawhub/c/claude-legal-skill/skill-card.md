## Description: <br>
Reviews legal contracts, NDAs, employment agreements, SaaS terms, and M&A documents to identify unfavorable terms, suggest redlines, and compare clauses to market standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youeshopent-debug](https://clawhub.ai/user/youeshopent-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, business users, and legal operations teams use this skill for first-pass contract review, due diligence, and negotiation preparation. It is intended to surface risks, key terms, missing provisions, and suggested redline language before qualified counsel reviews important agreements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contracts can contain confidential, privileged, or personal information. <br>
Mitigation: Use only documents you are authorized to submit, redact unnecessary sensitive data, and prefer enterprise or no-training AI environments for privileged matters. <br>
Risk: Contract review output can be incomplete, jurisdiction-dependent, or unsuitable as final legal advice. <br>
Mitigation: Use the skill for first-pass issue spotting and have qualified counsel review important agreements before relying on the output. <br>
Risk: Optional redline tooling may require installing and running third-party code. <br>
Mitigation: Verify any optional redline tooling before installation or execution, and run only trusted versions in an appropriate environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/youeshopent-debug/claude-legal-skill) <br>
- [CUAD Dataset](https://github.com/TheAtticusProject/cuad) <br>
- [LegalBench](https://hazyresearch.stanford.edu/legalbench/) <br>
- [ContractEval](https://arxiv.org/abs/2303.07389) <br>
- [legal-redline-tools](https://github.com/evolsb/legal-redline-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown review with tables and optional structured JSON redlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executive summaries, risk ratings, key terms, negotiation priorities, missing provisions, and suggested redline language.] <br>

## Skill Version(s): <br>
3.0.0 (source: artifact/skill.md frontmatter and artifact/CHANGELOG.md; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
