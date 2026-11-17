## Description:

Query and manage GitHub repositories: list repositories, check CI status, create issues, search repositories, and view recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent inspect GitHub repositories, review CI status and activity, search repositories, and create issues, repositories, or pull requests through authenticated GitHub access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad GitHub credentials can expose private repositories or account operations.

Mitigation: Use a fine-grained GitHub token restricted to selected repositories and only the permissions needed.

Risk: Write-capable actions such as create_issue, create_repo, and create_pull_request can make live GitHub changes.

Mitigation: Verify the target repository, visibility, branches, and proposed content before allowing the agent to run those actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/agent-github-workflow)
- [GitHub REST API endpoint](https://api.github.com)
- [GitHub personal access token settings](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown or structured text responses with repository details, CI status, activity summaries, created-resource links, and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated GitHub reads and live writes when the agent invokes write-capable actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
