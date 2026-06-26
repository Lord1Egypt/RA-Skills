## Description: <br>
Clawrouter is a local OpenClaw proxy that forwards model requests to the BlockRun hosted gateway for cost-aware LLM routing and exposes paid data and generation tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1bcmax](https://clawhub.ai/user/1bcmax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use Clawrouter to route LLM requests through BlockRun's hosted gateway, access gateway-backed models, and invoke paid market data, image, video, and prediction-market tools from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and request parameters are sent to a hosted gateway and downstream model providers. <br>
Mitigation: Use Clawrouter only for workloads appropriate for third-party hosted LLM APIs, and avoid sending data that should remain local. <br>
Risk: The local wallet key is stored in the OpenClaw config and can be used for paid model or tool calls if the host is compromised. <br>
Mitigation: Protect the config file, use an encrypted disk where appropriate, and fund only a small spending wallet intended for agent calls. <br>
Risk: The skill can make paid model, market data, image, video, and prediction-market tool calls. <br>
Mitigation: Review costs and routing behavior before use, and verify the npm package and release source before relying on it. <br>


## Reference(s): <br>
- [ClawRouter documentation](https://blockrun.ai/clawrouter.md) <br>
- [ClawRouter npm package](https://www.npmjs.com/package/@blockrun/clawrouter) <br>
- [BlockRun privacy policy](https://blockrun.ai/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and OpenClaw configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes prompts to a hosted gateway and may initiate paid model or tool calls using a locally stored wallet key.] <br>

## Skill Version(s): <br>
0.12.171 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
