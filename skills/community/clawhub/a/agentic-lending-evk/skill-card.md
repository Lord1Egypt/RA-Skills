## Description: <br>
Plans and executes guarded EVK lending workflows for Api3-backed markets, including oracle route resolution, feed readiness or funding, EVK deployment preparation, and optional post-deploy borrow proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi operators use this skill to plan, dry-run, and, with explicit approval, execute EVK lending market workflows backed by Api3 feeds. It helps agents resolve oracle paths, assess feed readiness, prepare deployments, and produce post-deploy borrow proof without overstating unsupported routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare or send real DeFi transactions, including feed funding, approvals, swaps, deployments, and borrow canaries. <br>
Mitigation: Use preview and preflight first, require explicit live execution approval, inspect persisted artifacts before reuse, and run with a dedicated signer. <br>
Risk: Private keys or signer material could be exposed through request files or CLI arguments. <br>
Mitigation: Keep signer material in environment variables such as LIVE_SIGNER_ENV and do not put private keys in committed files, request files, or command lines. <br>
Risk: Swap limits and approval settings can create loss or over-approval exposure. <br>
Mitigation: Set nonzero swap limits for live swaps and avoid unlimited approvals unless the operator explicitly accepts that risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daav3/agentic-lending-evk) <br>
- [Project homepage](https://github.com/daav3/agentic-lending-project) <br>
- [API reference](references/api_reference.md) <br>
- [Current capabilities and limits](references/current_capabilities.md) <br>
- [Summary contract](references/summary-contract.md) <br>
- [Live borrow checklist](references/live-borrow-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON request or proof configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce preflight, dry-run, or live-send-oriented instructions; live signing requires explicit user approval.] <br>

## Skill Version(s): <br>
0.1.16 (source: server release, CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
