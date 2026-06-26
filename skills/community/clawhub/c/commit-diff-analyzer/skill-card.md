## Description: <br>
Analyzes code changes between two git commits, including file modifications, additions, deletions, and commit context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afine907](https://clawhub.ai/user/afine907) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare two commits in a Git repository and understand commit metadata, changed files, diff details, and summary statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may display source code, commit history, file paths, and line-level changes from the current repository in chat. <br>
Mitigation: Use it only in repositories whose contents are appropriate to share with the active agent session. <br>
Risk: Commit comparisons can be misleading if the requested revisions are invalid, identical, or supplied in reverse chronological order. <br>
Mitigation: Validate both revisions with read-only Git commands and compare them in chronological order before summarizing changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and diff summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository commit metadata, file paths, change statistics, and line-by-line diff content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
