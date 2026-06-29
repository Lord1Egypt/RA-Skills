## Description: <br>
Generate Prd Prompt wraps the Mercury Spec Ops MCP Server to generate assembled PRD, codebase analysis, and bug analysis prompts and markdown templates for AI assistant workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and AI assistant operators use this skill to request generated PRD prompts, codebase analysis prompts, bug analysis prompts, and standard markdown templates based on selected technology stacks and analysis focus areas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the XiaoBenYang service API key in a local .env file. <br>
Mitigation: Use a workspace-specific key where possible, avoid sharing the workspace with the key present, and rotate or remove the key when access is no longer needed. <br>
Risk: Prompt parameters and optional project or bug context are sent to the XiaoBenYang remote API. <br>
Mitigation: Provide only content intended for that service, and avoid unrelated secrets or sensitive project data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alinklab/generate-prd-prompt) <br>
- [XiaoBenYang API Key Portal](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API Endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured API results presented as text or markdown prompt/template content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key and returns remote API results with minimal formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
