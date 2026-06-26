## Description: <br>
AI Skill for building EasyEDA Pro extension plugins, including creating, modifying, and debugging plugins, querying pro-api-types APIs, configuring extension.json, and handling i18n localization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonYANG170](https://clawhub.ai/user/JasonYANG170) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build EasyEDA Pro and JLCEDA extension plugins with verified API lookup, TypeScript generation guidance, extension configuration, localization support, and debugging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to control a live EasyEDA session through a local bridge. <br>
Mitigation: Use a dedicated workspace or account where possible and review agent actions before running bridge-driven debugging workflows. <br>
Risk: Generated plugin code or imported packages may execute in EasyEDA or during local builds. <br>
Mitigation: Review remote repositories, npm installs, and generated TypeScript before building or importing the extension. <br>
Risk: Login state, browser data, or debug logs may persist after development sessions. <br>
Mitigation: Avoid logging secrets and clear browser data or debug logs after use on shared machines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JasonYANG170/extension-dev-skill) <br>
- [API Reference](resources/api-reference.md) <br>
- [Common Pitfalls and Lessons Learned](resources/experience.md) <br>
- [EasyEDA Pro API SDK](https://github.com/easyeda/pro-api-sdk.git) <br>
- [Extension Dev MCP Tools](https://github.com/easyeda/extension-dev-mcp-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, JSON configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for review before execution in an EasyEDA Pro plugin workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
