## Description: <br>
Secure, sandboxed filesystem access enabling agents to list, read, write, create, move, delete, search files and directories within allowed paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuddhaSource](https://clawhub.ai/user/BuddhaSource) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure filesystem access for agents that need to inspect, create, update, search, organize, or summarize local files within explicitly allowed directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad filesystem allowlists can expose sensitive files or permit unwanted changes within approved folders. <br>
Mitigation: Configure the smallest specific folders possible, avoid credential and whole-home directories, and prefer read-only mode unless write access is required. <br>
Risk: Write, move, and delete operations can alter or remove important files in allowed directories. <br>
Mitigation: Review destructive actions before approving them and monitor filesystem server logs for unexpected access patterns. <br>
Risk: The setup installs or runs an upstream npm package for filesystem access. <br>
Mitigation: Consider pinning or verifying the upstream npm package before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BuddhaSource/filesystem-mcp) <br>
- [Model Context Protocol servers filesystem implementation](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) <br>
- [Model Context Protocol documentation](https://modelcontextprotocol.io/) <br>
- [Model Context Protocol security best practices](https://modelcontextprotocol.io/docs/concepts/security) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on allowed filesystem paths, read-only mode, MCP client configuration, and operational safety checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
