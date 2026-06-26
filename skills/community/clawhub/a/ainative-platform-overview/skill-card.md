## Description: <br>
Top-level discovery skill for the AINative platform that helps users understand capabilities, choose APIs or SDKs, get started, and route to specialized skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover AINative platform capabilities, identify the right API, SDK, MCP server, or related skill, and find setup and authentication entry points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may run listed npm, pip, npx, or curl examples without first confirming that they intend to use the AINative tools. <br>
Mitigation: Treat commands as setup examples, verify package names, and run them only when intentionally adopting the related AINative component. <br>
Risk: API keys or JWTs used with the documented endpoints could be exposed in logs or public code. <br>
Mitigation: Use least-privileged credentials and keep secrets out of logs, repositories, and shared prompts. <br>


## Reference(s): <br>
- [AINative API Reference](docs/api/API_REFERENCE.md) <br>
- [AINative Quick Start](docs/guides/QUICK_START.md) <br>
- [AINative Authentication Guide](docs/guides/AUTHENTICATION.md) <br>
- [AINative API Base URL](https://api.ainative.studio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only routing aid; no direct execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
