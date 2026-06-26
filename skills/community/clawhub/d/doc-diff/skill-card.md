## Description: <br>
Compare two documents or files and generate a structured diff report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document reviewers use this skill to compare two files or directories, inspect additions and deletions, and receive a concise Chinese-language change report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Comparing sensitive files or broad private directories may expose their contents in the generated diff report. <br>
Mitigation: Limit comparisons to intended files and directories, and avoid secrets, credentials, and private content unless that disclosure is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnoder-wgh/doc-diff) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cnoder-wgh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with diff output and Chinese-language summary sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local diff command output; binary documents may require text extraction before comparison.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
