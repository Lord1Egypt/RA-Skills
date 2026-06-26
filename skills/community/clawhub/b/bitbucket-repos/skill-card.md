## Description: <br>
Browse Bitbucket repositories, manage branches, review pull requests, and work with source code via the Bitbucket Cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect Bitbucket repositories, review pull requests, manage branches, and coordinate source-code workflows from an agent chat interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to Bitbucket resources available to the connected account. <br>
Mitigation: Review requested OAuth scopes during connection and revoke the ClawLink Bitbucket connection when it is no longer needed. <br>
Risk: Repository, branch, pull request, and issue write actions can change or delete Bitbucket resources. <br>
Mitigation: Preview and explicitly confirm create, update, merge, approve, comment, or delete actions before execution, especially destructive operations. <br>
Risk: Tool output is limited to repositories and workspaces accessible to the connected Bitbucket account. <br>
Mitigation: Verify the active Bitbucket connection and target workspace or repository before relying on results. <br>


## Reference(s): <br>
- [Bitbucket Skill on ClawHub](https://clawhub.ai/hith3sh/bitbucket-repos) <br>
- [Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/) <br>
- [Bitbucket Repository API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/) <br>
- [Bitbucket Pull Request API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=bitbucket-repos) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated ClawLink Bitbucket connection; write and destructive actions require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
