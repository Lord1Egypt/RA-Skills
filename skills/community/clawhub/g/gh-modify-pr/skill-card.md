## Description: <br>
Modify code based on GitHub PR review comments and create a local commit using gh + git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danie1Lin](https://clawhub.ai/user/danie1Lin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to address GitHub pull request review comments by inspecting PR metadata and inline comments, editing affected files, validating changes, and creating a local commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses configured GitHub and git access to read pull request data, clone or check out repositories, edit files, and create a local commit. <br>
Mitigation: Install it only when the agent should use that GitHub access, and review the resulting diff and commit before approving any push. <br>
Risk: Validation commands may run inside unfamiliar repositories while addressing review comments. <br>
Mitigation: Run only necessary validation, inspect commands before execution when risk is unclear, and avoid broad test or script execution without user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danie1Lin/gh-modify-pr) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/danie1Lin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summary with changed-file details, commit hash, branch name, and push status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local repository edits and a local git commit; push is only performed when requested or approved.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
