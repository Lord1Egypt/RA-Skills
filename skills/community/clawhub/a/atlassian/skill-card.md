## Description: <br>
Operate Atlassian Cloud APIs and CLIs across Jira, Confluence, Bitbucket, Trello, Admin, Forge, Compass, Opsgenie, and Statuspage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and operators use this skill to choose the correct Atlassian Cloud API or CLI, prepare safe terminal workflows, and automate read, write, search, and admin tasks across supported Atlassian products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with sensitive Atlassian admin, write, bulk, or destructive operations. <br>
Mitigation: Use least-privilege tokens and require explicit review before write, admin, bulk, or destructive operations. <br>
Risk: Atlassian credentials, API keys, and tokens may be exposed if pasted into prompts or saved in memory files. <br>
Mitigation: Keep secrets out of prompts and memory files; store only non-secret defaults and auth preferences. <br>
Risk: CLI installation or partner tooling can introduce a separate trust boundary. <br>
Mitigation: Verify CLI downloads and review partner CLI endpoints before using non-first-party tools. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/atlassian) <br>
- [Atlassian Cloud Product Map](artifact/product-map.md) <br>
- [Atlassian Auth and CLI Matrix](artifact/auth-and-clis.md) <br>
- [Jira Cloud Platform REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) <br>
- [Jira Software Cloud REST API](https://developer.atlassian.com/cloud/jira/software/rest/intro/) <br>
- [Jira Service Management Cloud REST API](https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/) <br>
- [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/) <br>
- [Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/intro/) <br>
- [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Cloud Admin REST APIs](https://developer.atlassian.com/cloud/admin/rest-apis/) <br>
- [Atlassian CLI Commands](https://developer.atlassian.com/cloud/acli/reference/commands/) <br>
- [Forge CLI Reference](https://developer.atlassian.com/platform/forge/cli-reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, API endpoints, JSON-oriented guidance, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce curl, jq, acli, forge, and product-specific API guidance; requires curl or jq according to release metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
