## Description: <br>
Complete code review workflow for GitCode PRs, combining automated security scanning with manual review, formatted findings, and optional PR comment posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guitenbay](https://clawhub.ai/user/guitenbay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review GitCode pull requests, combine automated scan results with manual analysis, select the highest-priority issues, and prepare review comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The posting script can publish PR comments immediately after showing its preview. <br>
Mitigation: Inspect generated comments before running any posting step, and require an explicit human approval gate around execution. <br>
Risk: GitCode tokens are required and may be exposed if passed carelessly. <br>
Mitigation: Use a least-privilege, short-lived token and prefer environment-variable handling over command-line arguments or URLs. <br>
Risk: Temporary review files may contain pull request code, scan results, or comment drafts. <br>
Mitigation: Run from a dedicated workspace, verify the temp directory contents, and clean temporary files after review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guitenbay/code-review-for-gitcode) <br>
- [GitCode PR comments API](https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/comments) <br>
- [GitCode PR diff API](https://gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON review artifacts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate temporary JSON files for scan results, selected issues, and formatted PR comments.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
