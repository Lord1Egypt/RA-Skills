## Description:

Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query and manage GitHub repositories from an agent, including listing repositories, checking CI status, creating issues and repositories, searching repositories, viewing recent commits, and creating pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent changes to GitHub repositories, including creating issues, repositories, and pull requests.

Mitigation: Use fine-grained GitHub tokens limited to the intended repositories and permissions, and confirm the target repository, visibility, branch, title, and body before invoking write actions.

Risk: The pull request action is under-documented and has weak argument controls.

Mitigation: Manually review or remediate the pull request action before routine use, and require explicit owner, repository, source branch, target branch, title, and body review.

Risk: Unrestricted issue extra fields may pass unexpected values to GitHub issue creation.

Mitigation: Restrict or review extra issue fields before execution and prefer a minimal allowlist for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/dev-workflow-automation)
- [Publisher profile](https://clawhub.ai/user/yesong-hue)
- [GitHub personal access token setup](https://github.com/settings/tokens)
- [GitHub REST API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Agent-facing text or Markdown with GitHub API result summaries, resource URLs, and setup snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub credentials through GITHUB_TOKEN/GITHUB_USERNAME or github.token/github.username configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact package.json reports 2.0.0 and artifact _meta.json/index exports report 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
