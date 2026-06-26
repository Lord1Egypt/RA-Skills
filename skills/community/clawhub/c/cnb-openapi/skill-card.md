## Description: <br>
Interacts with the CNB (Cloud Native Build) Open API for code management and development collaboration, including querying projects, repositories, issues, pull requests, and related development data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sixther-dc](https://clawhub.ai/user/sixther-dc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to execute authenticated CNB API operations for repository, issue, pull request, build, workspace, release, organization, member, registry, and security workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated CNB account and repository authority. <br>
Mitigation: Use a least-privilege CNB_TOKEN, avoid storing it in shared shell profiles or logs, and limit access to the repositories and organizations required for the task. <br>
Risk: State-changing CNB operations can affect repositories, permissions, builds, workspaces, pull requests, releases, registries, and AI auto-PR actions. <br>
Mitigation: Require explicit workflow confirmation before POST, PUT, PATCH, DELETE, merge, permission, build, workspace, and AI auto-PR actions are executed. <br>
Risk: An incorrect CNB_API_ENDPOINT could send authenticated requests to an unintended endpoint. <br>
Mitigation: Verify CNB_API_ENDPOINT before use and prefer the documented default endpoint unless a trusted alternate endpoint is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sixther-dc/cnb-openapi) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Node usage](docs/node.md) <br>
- [Go usage](docs/go.md) <br>
- [Claude Code usage](docs/claudecode.md) <br>
- [OpenClaw usage](docs/openclaw.md) <br>
- [Build status API](references/build/getbuildstatus.md) <br>
- [Repository details API](references/repositories/getbyid.md) <br>
- [Issue details API](references/issues/getissue.md) <br>
- [Pull request details API](references/pulls/getpull.md) <br>
- [Security overview API](references/security/getreposecurityoverview.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown with curl commands, CNB API response summaries, and JSON data when returned by the API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and CNB_TOKEN; CNB_API_ENDPOINT is optional and defaults to https://api.cnb.cool.] <br>

## Skill Version(s): <br>
1.18.9 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
