## Description: <br>
Adds observability and tracing to AI/LLM applications using the Anyway SDK for monitoring calls to providers like OpenAI and Anthropic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremy-any](https://clawhub.ai/user/jeremy-any) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to have an agent add Anyway SDK observability, cost tracking, and tracing to Python or JavaScript AI applications that call LLM providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracing may capture prompts, responses, costs, provider metadata, or other sensitive application data. <br>
Mitigation: Review instrumentation scope, redact sensitive fields where needed, and align trace retention with the application's privacy and compliance requirements. <br>
Risk: Incorrect API key handling could expose credentials while configuring the SDK. <br>
Mitigation: Use environment variables or a secrets manager, and review generated code to confirm credentials are never hardcoded. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeremy-any/anyway-traces) <br>
- [Anyway documentation index](https://docs.anyway.sh/llms.txt) <br>
- [Anyway skill source](https://docs.anyway.sh/skills.md) <br>
- [Anyway quickstart](https://docs.anyway.sh/quickstart) <br>
- [Python SDK tracing](https://docs.anyway.sh/sdk/python/tracing) <br>
- [JavaScript SDK tracing](https://docs.anyway.sh/sdk/js/tracing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose SDK installation, environment variable setup, tracing initialization, provider instrumentation, and workflow or task spans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
