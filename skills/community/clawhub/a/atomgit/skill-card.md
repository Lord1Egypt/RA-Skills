## Description: <br>
AtomGit/GitCode repository-management skill that helps an agent call OpenAPI v5 for users, repositories, issues, pull requests, files, branches, and related account operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to operate AtomGit or GitCode accounts and repositories through documented API calls, including user lookup, repository management, issues, pull requests, branches, files, releases, webhooks, and organization or enterprise endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad AtomGit/GitCode account and repository authority through raw API calls. <br>
Mitigation: Use a dedicated minimally scoped token and avoid broad long-lived credentials where possible. <br>
Risk: Documented operations include destructive or sensitive changes such as delete, transfer, merge, collaborator, webhook, SSH-key, file, release, organization, and enterprise actions. <br>
Mitigation: Require explicit human confirmation before executing sensitive account, repository, or organization changes. <br>
Risk: The skill documents AI/media and OAuth endpoints beyond ordinary repository management. <br>
Mitigation: Limit use to intended repository-management workflows unless the operator has reviewed and approved those additional endpoint categories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/atomgit) <br>
- [GitCode API documentation](https://docs.gitcode.com/docs/apis/) <br>
- [GitCode token management](https://gitcode.com/setting/token-classic) <br>
- [AtomGit token management](https://atomgit.com/setting/token-classic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ATOMGIT_TOKEN credential and may produce raw AtomGit/GitCode API requests.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
