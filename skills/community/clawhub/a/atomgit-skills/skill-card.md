## Description: <br>
Helps agents safely inspect and change AtomGit repositories, pull requests, issues, branches, releases, tags, permissions, organizations, enterprises, kanban boards, webhooks, and AIHub features through the AtomGit MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylezhang](https://clawhub.ai/user/kylezhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with AtomGit resources through a preconfigured AtomGit MCP server. It supports repository, pull request, issue, organization, enterprise, webhook, and AIHub workflows while applying token and confirmation safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AtomGit access requires an ATOMGIT_TOKEN, which can expose repository or account permissions if mishandled. <br>
Mitigation: Store the token in the MCP client environment or a secret store, never paste it into chat or repository files, and start with the smallest token scope needed. <br>
Risk: Repository writes, membership or permission changes, enterprise administration, webhook changes, and dangerous-tool use can have broad or irreversible effects. <br>
Mitigation: Require explicit user confirmation before these operations and prefer read operations before mutations. <br>
Risk: The skill depends on an external AtomGit MCP server and its exposed runtime tool set. <br>
Mitigation: Review the referenced MCP server before installation, configure it manually at the client level, and match the exact tool names exposed by the runtime. <br>


## Reference(s): <br>
- [AtomGit Skill Source](https://atomgit.com/zkxw2008/AtomGit-Skills) <br>
- [AtomGit MCP Server](https://atomgit.com/zkxw2008/AtomGit-MCP-Server) <br>
- [AtomGit MCP Server npm Package](https://www.npmjs.com/package/@atomgit.com/atomgit-mcp-server) <br>
- [Setup And Safety](references/setup-and-safety.md) <br>
- [Repositories](references/repositories.md) <br>
- [Pull Requests](references/pull-requests.md) <br>
- [Issues](references/issues.md) <br>
- [Organizations](references/organizations.md) <br>
- [Enterprises](references/enterprises.md) <br>
- [Webhooks](references/webhooks.md) <br>
- [AIHub](references/aihub.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with AtomGit MCP method names and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a preconfigured AtomGit MCP server and ATOMGIT_TOKEN.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
