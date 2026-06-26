## Description: <br>
DaoReview reviews .docx, .txt, and .md documents in Chinese, scoring structure, content quality, formatting, logic, and actionability while suggesting improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[douglasliu](https://clawhub.ai/user/douglasliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users use this skill to inspect uploaded or referenced documents and receive an objective review report with a score, strengths, issues, and concrete improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the contents of user-provided documents, which may expose confidential, regulated, or sensitive information during review. <br>
Mitigation: Use it only with documents appropriate for the agent environment, and avoid sensitive files unless that review is authorized. <br>
Risk: Document extraction may run local commands such as pandoc, docx2txt, unzip, sed, or cat against user-supplied paths. <br>
Mitigation: Review file paths before extraction and run the skill in an environment where local file access is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report in Chinese, with shell commands used when extracting document text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores documents out of 100 across five weighted review dimensions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
