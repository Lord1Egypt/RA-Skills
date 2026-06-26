## Description: <br>
Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to let an OpenClaw assistant inspect GitHub repositories, check CI status and recent activity, and create issues, repositories, or pull requests with the configured GitHub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent GitHub changes with the authority granted to the configured token. <br>
Mitigation: Use the narrowest possible GitHub token, prefer public-only or fine-grained permissions when possible, and install only when agent-mediated GitHub writes are intended. <br>
Risk: Write actions can affect repository visibility, issues, branches, and pull-request targets. <br>
Mitigation: Manually confirm repository names, visibility, issue content, branches, and pull-request targets before allowing mutating actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yesong-hue/dev-workflow-automation) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>
- [GitHub REST API endpoint](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Structured repository, CI, issue, repository-creation, and pull-request results with text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITHUB_TOKEN/GITHUB_USERNAME environment variables or github.token/github.username configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
