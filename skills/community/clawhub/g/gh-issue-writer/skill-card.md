## Description: <br>
Draft well-structured GitHub issues from a description, error, or idea, with support for bug reports, feature requests, enhancements, tasks, and optional user-directed submission through GitHub tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to turn brief problem reports, ideas, or error messages into structured GitHub issues with clear titles, labels, metadata suggestions, and review-ready issue bodies. When explicitly approved, it can help submit the issue through the GitHub CLI or GitHub API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare labels, titles, issue bodies, and target repository details that may be incorrect or disclose sensitive project information if submitted without review. <br>
Mitigation: Review the full issue title, body, labels, and target repository before approving submission. <br>
Risk: Optional GitHub issue submission uses GitHub credentials through the GitHub CLI or GH_TOKEN. <br>
Mitigation: Use a least-privileged GitHub token and only approve submission after confirming the destination repository and issue content. <br>


## Reference(s): <br>
- [GitHub Issue Template Documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests) <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/gh-issue-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with optional shell commands and JSON API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafting works without credentials; submission requires GitHub CLI authentication or a GH_TOKEN fallback.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
