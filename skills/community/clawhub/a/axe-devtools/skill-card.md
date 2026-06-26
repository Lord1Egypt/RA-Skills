## Description: <br>
Accessibility testing and remediation using the axe MCP Server for web pages, components, forms, navigation, modals, tables, images, and other user-facing markup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanb](https://clawhub.ai/user/dylanb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill while creating or modifying UI code to scan live pages for accessibility violations and request remediation guidance for specific issues. It can also guide static accessibility review when no live page is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a Dockerized axe MCP server and uses networked Deque axe services. <br>
Mitigation: Use it only where Docker execution and Deque axe MCP network usage are approved, and consider pinning the Docker image to a specific version or digest. <br>
Risk: Accessibility scans and remediation requests may involve page URLs, HTML, or issue details that could be sensitive. <br>
Mitigation: Avoid scanning confidential pages or sending sensitive HTML unless the provider data flow is approved for that content. <br>
Risk: The skill requires an Axe API key and remediation calls consume the organization's AI credits. <br>
Mitigation: Use a rotatable API key, scope access according to organizational policy, and monitor usage for expected credit consumption. <br>


## Reference(s): <br>
- [Axe MCP Server product page](https://www.deque.com/axe/mcp-server/) <br>
- [ClawHub skill page](https://clawhub.ai/dylanb/axe-devtools) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance, Code] <br>
**Output Format:** [JSON-RPC responses and text remediation guidance with code fix suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyze requires a URL; remediation requires a rule ID, element HTML, issue remediation text, and optionally a page URL.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
