## Description: <br>
Verify claims, numbers, and facts in markdown drafts against source data before publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content authors, and documentation reviewers use this skill to check markdown drafts against local project evidence before publication. It highlights confirmed, unverifiable, and contradicted claims and suggests corrections for contradicted claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads named project files, memory markdown logs, git history, score JSON files, and a local status service. <br>
Mitigation: Install it only in workspaces where those local reads are acceptable for the review task. <br>
Risk: Using --output with an existing path can overwrite a previous report. <br>
Mitigation: Use a fresh report filename for each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/fact-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown verification report with claim status lines and summary counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also write the same report to a user-specified markdown file via --output.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
