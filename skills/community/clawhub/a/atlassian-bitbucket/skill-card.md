## Description: <br>
Browse Bitbucket Cloud repos, review pull requests, read diffs, check branches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pejovicvuk](https://clawhub.ai/user/pejovicvuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Bitbucket Cloud repositories, pull requests, diffs, comments, branches, commits, and source files through read-only API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Bitbucket token can read repository code, pull requests, comments, diffs, branch metadata, and source files available to that token. <br>
Mitigation: Use a separate Bitbucket API token scoped to read-only repository and pull-request permissions, and limit workspace access where possible. <br>
Risk: Agent responses may expose Bitbucket data when a user intended to inspect local or other-hosted code. <br>
Mitigation: Be explicit when requesting Bitbucket access and verify the target workspace, repository, branch, and pull request before using returned content. <br>
Risk: Command results can be paginated or capped, which can make repository, pull request, branch, commit, or search views incomplete. <br>
Mitigation: Treat limited results as partial and request follow-up queries or narrower searches when completeness matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pejovicvuk/atlassian-bitbucket) <br>
- [Publisher Profile](https://clawhub.ai/user/pejovicvuk) <br>
- [Bitbucket Cloud API](https://api.bitbucket.org/2.0) <br>
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; command results are JSON or raw text from Bitbucket Cloud.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Bitbucket API wrapper; repository, pull request, branch, file, search, and diff results may be paginated or limited.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
