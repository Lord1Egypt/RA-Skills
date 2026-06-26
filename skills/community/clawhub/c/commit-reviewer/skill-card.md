## Description: <br>
Checks one or more Git revisions against a requirement or bug description and gives itemized conclusions about whether the commits actually fix the issue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carpedx](https://clawhub.ai/user/carpedx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review one or more Git commits against a stated requirement or bug report, using the real diff to judge whether the change fully fixes the issue, partially fixes it, or leaves risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private commit diffs and repository metadata to the agent during review. <br>
Mitigation: Run it only on repositories and commits the agent is allowed to inspect, and set COMMIT_REVIEWER_WORK_ROOT to the narrowest useful workspace. <br>
Risk: Git remote URLs shown in collected context may contain tokens or other sensitive values. <br>
Mitigation: Avoid credential-bearing remote URLs before using the skill, or sanitize repository remotes in the target workspace. <br>
Risk: Large patches may be truncated by the context collection script. <br>
Mitigation: Increase COMMIT_REVIEWER_PATCH_LINES or inspect the omitted diff manually when the truncated section could affect the fix judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carpedx/commit-reviewer) <br>
- [Publisher profile](https://clawhub.ai/user/carpedx) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured review conclusions and supporting evidence from Git context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs Chinese review prose; commit patch output is capped by COMMIT_REVIEWER_PATCH_LINES when gathering context.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
