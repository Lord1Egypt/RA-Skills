## Description: <br>
Verifies BibTeX files for hallucinated or fabricated references by cross-checking entries against CrossRef, arXiv, and DBLP and reporting verified, suspect, or not-found results with field-level mismatch details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloml0326](https://clawhub.ai/user/helloml0326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and writing teams use this skill to audit .bib files for fabricated, hallucinated, or mis-cited academic references before submitting papers or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bibliography metadata is sent to CrossRef, arXiv, and DBLP during verification. <br>
Mitigation: Only check bibliographies whose citation metadata is acceptable to share with those services. <br>
Risk: The workflow installs and runs third-party Python packages. <br>
Mitigation: Install py-openjudge and litellm in a virtual environment and review or pin dependencies before use. <br>
Risk: Providing a CrossRef email can improve rate limits but shares that email with CrossRef. <br>
Mitigation: Provide a CrossRef email only when the rate-limit benefit is needed. <br>


## Reference(s): <br>
- [Full pipeline options](../paper-review/reference.md) <br>
- [Combined PDF review and BibTeX verification](../paper-review/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/helloml0326/bib-verify) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with status labels, field-level mismatch details, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the report to a user-selected Markdown output path when the underlying command is run with --output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
