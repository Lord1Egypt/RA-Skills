## Description: <br>
Command-line code review assistant for generating review-style reports about bugs, security issues, code style, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to request code review-style summaries for files, git diffs, and pull requests, including issues grouped by severity and category. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises real code and security review while evidence.security reports that it returns canned reports. <br>
Mitigation: Treat its output as illustrative guidance only and do not rely on it for merge decisions, CI gates, vulnerability detection, or security signoff without replacing the canned behavior with real analysis. <br>
Risk: Pull request review commands mention GitHub integration and GITHUB_TOKEN usage. <br>
Mitigation: Provide only the minimum required token permissions and avoid exposing secrets in command output or shared logs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference GITHUB_TOKEN for pull request review commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
