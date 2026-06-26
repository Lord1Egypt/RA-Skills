## Description: <br>
Manage Biznet Gio cloud infrastructure, including servers, VMs, storage, and IPs, through the Biznet Gio CLI and MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biznetgio](https://clawhub.ai/user/biznetgio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Biznet Gio cloud resources from an agent workflow. It supports authentication guidance, read-only inventory checks, and reviewed create, update, state-change, and delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate cloud infrastructure and uses sensitive Biznet Gio credentials. <br>
Mitigation: Use the browser-based biznetgio login flow, avoid embedding API keys in commands or configuration files, and use the least-privileged account available. <br>
Risk: Create, update, delete, rebuild, and state-change operations can affect availability or destroy resources. <br>
Mitigation: Review every infrastructure-changing command before execution, and require explicit confirmation for destructive actions. <br>
Risk: Saved credentials can remain available after the task is complete. <br>
Mitigation: Run biznetgio logout when finished to remove the local credential file. <br>


## Reference(s): <br>
- [Biznet Gio CLI homepage](https://github.com/BiznetGIO/biznetgio-cli) <br>
- [Biznet Gio CLI npm package](https://www.npmjs.com/package/@biznetgio/cli) <br>
- [Biznet Gio MCP npm package](https://www.npmjs.com/package/@biznetgio/mcp) <br>
- [Biznet Gio API OpenAPI specification](https://api.portal.biznetgio.com/v1/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional CLI table or JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that operate cloud infrastructure and credential setup guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
