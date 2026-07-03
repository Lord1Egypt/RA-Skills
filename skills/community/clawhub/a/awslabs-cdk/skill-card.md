## Description: <br>
Provides AWS CDK best-practice guidance, infrastructure-as-code patterns, CDK Nag rule explanations, and related AWS application-building advice through a Xiaobenyang-hosted API wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building AWS CDK applications use this skill to request CDK best-practice guidance, CDK Nag rule explanations, AWS Solutions Constructs discovery, GenAI CDK construct search, and related Lambda layer documentation pointers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an XBY_APIKEY and saves it locally for reuse. <br>
Mitigation: Use a dedicated Xiaobenyang API key, avoid sharing AWS credentials or other secrets, and remove XBY_APIKEY from .env when the skill should no longer retain access. <br>
Risk: CDK guidance and submitted parameters are handled through a third-party Xiaobenyang-hosted service. <br>
Mitigation: Install only when that third-party dependency is acceptable, and review returned CDK guidance before applying it to infrastructure code. <br>
Risk: Some advertised functions are marked deprecated in the artifact. <br>
Mitigation: Prefer the recommended replacement service for deprecated workflows and treat deprecated-function output as advisory. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cainingnk/skills/awslabs-cdk) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [Xiaobenyang API key portal](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API service](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown-style guidance with raw API results summarized for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY and may send user-provided parameters or code snippets to the Xiaobenyang API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
