## Description: <br>
When the user has a new development idea, search GitHub first for open-source projects to fork as a starting point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdwhisper](https://clawhub.ai/user/gdwhisper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill during early project ideation to search GitHub for open-source repositories that may be suitable to fork, extend, or study before building from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad coding requests and steer the agent toward GitHub search before the user has asked for external project reuse. <br>
Mitigation: Install it only in environments where proactive GitHub discovery is desired, and confirm with the user before recommending a fork as the implementation path. <br>
Risk: Helper scripts can run shell commands with poorly scoped inputs. <br>
Mitigation: Avoid untrusted script options or repository names until the scripts use a safer HTTP client or argument-array subprocess call. <br>
Risk: The skill may use GitHub credentials for higher API limits. <br>
Mitigation: Use a minimal GitHub token only when needed and avoid granting broader scopes than repository search requires. <br>
Risk: Forking third-party repositories can carry license and reuse obligations. <br>
Mitigation: Review repository licenses and project terms before forking, extending, or shipping derived work. <br>


## Reference(s): <br>
- [Fork-It ClawHub listing](https://clawhub.ai/gdwhisper/fork-it) <br>
- [gdwhisper ClawHub profile](https://clawhub.ai/user/gdwhisper) <br>
- [GitHub Search API v3](https://api.github.com/search/repositories) <br>
- [GitHub REST API repositories endpoint](https://api.github.com/repos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GITHUB_TOKEN for higher GitHub API rate limits; review repository licenses before forking third-party code.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
