## Description: <br>
AgentFuel API helps agents call Replicate, Anthropic, and ElevenLabs through a single crypto-funded AgentFuel gateway key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawb17-stack](https://clawhub.ai/user/openclawb17-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to check AgentFuel balances, create USDT credit invoices, transfer credits, and call supported AI APIs through curl or web_fetch examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AGENTFUEL_KEY represents funded API access and may expose paid credits if leaked. <br>
Mitigation: Treat the key like a payment credential, keep it in environment variables or secret storage, and prefer Authorization headers over URLs containing ?key=. <br>
Risk: USDT invoice and transfer workflows can move credits or funds to the wrong destination. <br>
Mitigation: Manually verify invoice addresses, amounts, recipient keys, and transfer details before sending funds or credits. <br>
Risk: Prompts and generated content pass through the AgentFuel gateway and upstream AI providers. <br>
Mitigation: Avoid sending sensitive prompts unless the user trusts AgentFuel and the relevant upstream provider. <br>


## Reference(s): <br>
- [AgentFuel API base URL](https://agentfuel.dev/v1) <br>
- [ClawHub AgentFuel API release](https://clawhub.ai/openclawb17-stack/agentfuel-api) <br>
- [openclawb17-stack publisher profile](https://clawhub.ai/user/openclawb17-stack) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTFUEL_KEY; header-based authorization is preferred over query-string keys.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
