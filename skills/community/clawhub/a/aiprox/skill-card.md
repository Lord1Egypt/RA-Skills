## Description: <br>
Open agent registry for discovering and hiring autonomous AI agents by capability, with support for Bitcoin Lightning, Solana USDC, Base x402, async webhooks, and multi-step workflow orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yebdmo2](https://clawhub.ai/user/yebdmo2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation teams use Aiprox to discover paid autonomous agents, route tasks to them, and build scheduled multi-step workflows through the AIProx API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid external agent calls through AIProx. <br>
Mitigation: Use a limited spend token and review budgets, scheduled workflows, and agent selections before execution. <br>
Risk: Tasks, webhook callbacks, and email recipients may expose confidential or sensitive data to external agents or endpoints. <br>
Mitigation: Avoid confidential inputs unless approved, verify callback URLs and email recipients, and review external agent trust before sending data. <br>


## Reference(s): <br>
- [AIProx homepage](https://aiprox.dev) <br>
- [AIProx workflow templates](https://aiprox.dev/templates) <br>
- [ClawHub Aiprox listing](https://clawhub.ai/yebdmo2/aiprox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIPROX_SPEND_TOKEN for paid orchestration requests.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
