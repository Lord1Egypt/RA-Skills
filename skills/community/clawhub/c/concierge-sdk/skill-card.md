## Description: <br>
Concierge SDK helps developers build Python MCP servers, tools, resources, and agentic applications with staged tool disclosure, shared state, semantic search, widgets, HTTP and stdio transports, and cloud deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArnavBalyan](https://clawhub.ai/user/ArnavBalyan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill for guidance and examples to install Concierge SDK, build or convert MCP servers, configure state and transports, add widgets, and deploy Concierge projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional telemetry, cloud deployment, and PostgreSQL state features can involve database or cloud credentials. <br>
Mitigation: Leave telemetry and PostgreSQL credentials unset unless needed, and scope any database or cloud tokens narrowly. <br>
Risk: Using the Concierge package in sensitive systems without review could introduce dependency or configuration risk. <br>
Mitigation: Install in a virtual environment or container, and review the package and source before use in sensitive environments. <br>


## Reference(s): <br>
- [Concierge source repository](https://github.com/concierge-hq/concierge) <br>
- [concierge-sdk on PyPI](https://pypi.org/project/concierge-sdk) <br>
- [Concierge issue tracker](https://github.com/concierge-hq/concierge/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional environment variable guidance for PostgreSQL state, telemetry, and cloud deployment credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
