## Description: <br>
Enterprise-grade code review agent. Reviews PRs, diffs, or code files for security vulnerabilities, performance issues, error handling gaps, architecture smells, and test coverage. Works with any language, any repo, no dependencies required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub PRs, local diffs, files, or pasted code for security, performance, error handling, architecture, reliability, and test coverage before merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read code, diffs, and PR details supplied for review. <br>
Mitigation: Use it only on repositories and code the agent is allowed to access. <br>
Risk: Optional GitHub CLI workflows can post PR comments or reviews. <br>
Mitigation: Confirm the active GitHub account, target repository, and comment-posting permission before running GitHub review commands. <br>
Risk: Review findings and suggested fixes may be incomplete or incorrect. <br>
Mitigation: Have maintainers validate findings and changes before merge or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-code-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown code review reports with tables, severity findings, SPEAR scores, and optional code or shell command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub PR review comments, prioritized recommendations, and checklist items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
