## Description: <br>
Read-only Morpho-first agentic lending planning for Api3-backed markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan Morpho market or market-set readiness for selected collateral and borrow assets, resolve Api3 oracle routes, inspect feed readiness, and prepare deployment or verification handoffs without signing, funding, broadcasting, or submitting transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake planner output, cached artifacts, or prior-run context for live on-chain verification. <br>
Mitigation: Require a usable RPC endpoint before claiming on-chain verification and clearly separate live RPC results from cached or prior-run information. <br>
Risk: Requests involving wallets, private keys, funding, deployment, broadcasts, or transaction submission are outside the skill's read-only boundary. <br>
Mitigation: Do not provide private keys, seed phrases, wallet signing access, or permission to broadcast transactions; hand off any funding or deployment step to an operator. <br>


## Reference(s): <br>
- [Current capabilities and limits](references/current_capabilities.md) <br>
- [Morpho oracle adapter, Api3-backed](references/morpho-oracle-adapter.md) <br>
- [Morpho-first workflow](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/daav3/agentic-lending-morpho-readonly) <br>
- [Publisher profile](https://clawhub.ai/user/daav3) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with read-only command examples and handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates planning-only findings from operator-required actions and live RPC verification results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
