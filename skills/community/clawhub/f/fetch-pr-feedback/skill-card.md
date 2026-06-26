## Description: <br>
Fetch unresolved review comments from a PR and evaluate with receive-feedback skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to collect unresolved GitHub pull request feedback, format it by reviewer, and route it through a feedback-processing workflow before making code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads PR review comments through the user's GitHub CLI session and passes them into a feedback-processing workflow. <br>
Mitigation: Install only if that access is expected, and review formatted feedback plus any proposed code changes before accepting them. <br>
Risk: Reviewer comments from bots or external contributors may contain misleading or untrusted instructions. <br>
Mitigation: Treat fetched comments as feedback to evaluate, not as commands to execute automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/fetch-pr-feedback) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/anderskev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured reviewer feedback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches GitHub PR comments through the GitHub CLI session; excludes PR author, current user, and resolved review threads by default.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
