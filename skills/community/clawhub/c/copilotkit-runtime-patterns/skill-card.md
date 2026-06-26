## Description: <br>
Provides server-side runtime patterns for CopilotKit endpoints, remote agent configuration, middleware, security, and performance optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeneralJerel](https://clawhub.ai/user/GeneralJerel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill when setting up or refactoring CopilotKit runtime endpoints, registering remote agents, adding middleware, and applying security or streaming-performance patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication tokens or user context may be passed incorrectly when applying the examples. <br>
Mitigation: Review token handling and require authentication middleware before agent execution. <br>
Risk: Overly broad CORS settings can expose a CopilotKit runtime endpoint to unwanted frontend origins. <br>
Mitigation: Restrict CORS to the actual production frontend origins. <br>
Risk: Unbounded runtime access can exhaust LLM or agent execution budget. <br>
Mitigation: Configure rate limits by authenticated user or API key. <br>
Risk: Persistent conversation storage can introduce privacy and retention obligations. <br>
Mitigation: Match storage configuration to the application's privacy and retention requirements. <br>


## Reference(s): <br>
- [CopilotKit Documentation](https://docs.copilotkit.ai) <br>
- [CopilotKit GitHub Repository](https://github.com/CopilotKit/CopilotKit) <br>
- [CopilotRuntime Reference](https://docs.copilotkit.ai/reference/v1/classes/CopilotRuntime) <br>
- [CopilotKit Self Hosting Guide](https://docs.copilotkit.ai/guides/self-hosting) <br>
- [CopilotKit Security Guide](https://docs.copilotkit.ai/guides/security) <br>
- [CopilotKit Multi-Agent Flows](https://docs.copilotkit.ai/coagents/multi-agent-flows) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference skill for agent-facing implementation guidance; no runtime execution behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact document version 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
