## Description: <br>
Multi-agent code review for pull requests that checks for bugs, CLAUDE.md compliance, git history context, and previous PR comments, using confidence scoring to filter false positives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonbraun](https://clawhub.ai/user/emersonbraun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests for significant, verifiable bugs and repository-specific guidance compliance before merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish GitHub pull request comments using the active GitHub CLI account. <br>
Mitigation: Confirm the repository, pull request number, and GitHub account before use, and require the agent to draft the comment for approval before posting. <br>


## Reference(s): <br>
- [Review Patterns](references/review-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/emersonbraun/eb-code-review) <br>
- [Publisher profile](https://clawhub.ai/user/emersonbraun) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review comments with links to relevant files, lines, and supporting evidence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post a GitHub pull request comment through the active GitHub CLI account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
