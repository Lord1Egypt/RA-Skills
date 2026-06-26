## Description: <br>
Guides an agent through branch checks, safe commits, pushing, and pull request creation or updates with a concise summary and test plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to move a prepared working tree through a safe git delivery flow: inspect changes, commit the right files, push a branch, and create or update a pull request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can commit, push, and open or update pull requests in the current repository. <br>
Mitigation: Confirm the repository, branch, remote, authenticated account, staged files, and diff before allowing the workflow to run. <br>
Risk: Unrelated files or secrets could be included if the working tree is not reviewed. <br>
Mitigation: Review staged changes and exclude unrelated or sensitive files before committing and pushing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/claude-code-git-commit-pr-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with shell command execution and pull request text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create commits, push branches, and open or update pull requests in the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
