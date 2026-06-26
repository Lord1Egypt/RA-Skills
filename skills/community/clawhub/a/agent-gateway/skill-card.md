## Description: <br>
Smart multi-model routing for Claude, GPT, Gemini, and local Ollama models with cost optimization, fallback chains, and usage tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mackding](https://clawhub.ai/user/mackding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to start or configure a local OpenAI-compatible gateway that routes chat completion requests across multiple model providers with fallback, cost, and usage controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway may send prompts, request metadata, and provider credentials to configured cloud model providers. <br>
Mitigation: Expose only the API keys needed for the intended providers, configure provider-side limits, and use local Ollama when requests must stay local. <br>
Risk: The real gateway behavior depends on the external @claws-shield/cli npm package. <br>
Mitigation: Review and pin the CLI package version before use, and install it only from a trusted package source. <br>
Risk: The artifact wrapper script does not start the gateway directly in skill mode. <br>
Mitigation: Use the documented CLI command to start the gateway and verify the local endpoint before routing agent traffic through it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mackding/agent-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/mackding) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local gateway startup guidance for an OpenAI-compatible chat completions endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
