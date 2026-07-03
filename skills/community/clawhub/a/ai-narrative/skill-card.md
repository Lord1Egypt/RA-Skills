## Description: <br>
AI-generated market narrative based on current regime and data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to fetch current AI-generated crypto market narrative as context for reasoning summaries and strategy decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses EVM_PRIVATE_KEY for automatic x402 payment authorization, which could expose funds if the key is reused or overfunded. <br>
Mitigation: Use only a dedicated low-balance wallet for EVM_PRIVATE_KEY and do not reuse wallets that hold important funds. <br>
Risk: Each agent request can trigger a paid on-chain-backed authorization. <br>
Mitigation: Monitor usage and cap calls before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/ai-narrative) <br>
- [APEX Runner AI Narrative signal](https://apexrunner.ai/signals/ai-narrative) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code examples and JSON API response content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
