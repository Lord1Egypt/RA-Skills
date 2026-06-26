## Description: <br>
Consolidate and respond to external feedback on pull requests and issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to collect AI review feedback, classify findings, prepare review summaries, manage formal review decisions, and track deferred follow-up work for pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post GitHub review summaries or formal review content and may write deferred-review tracking updates when invoked. <br>
Mitigation: Invoke it deliberately, use --interactive when draft approval is needed, and review repository tracking files after runs that register deferred findings. <br>
Risk: Review consolidation can carry forward incorrect or misleading external AI feedback. <br>
Mitigation: Verify findings against the checked-out pull request worktree before accepting, rejecting, posting, or deferring them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/consolidate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown with inline shell commands and workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May draft GitHub review summaries, formal review text, deferred-finding tracking updates, and next-action prompts.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
