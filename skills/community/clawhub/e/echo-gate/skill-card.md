## Description: <br>
Echo Gate helps agents register, expose, call, secure, audit, and operate local-first tools through the BuiltByEcho gateway, including API keys, receipts, approvals, spend limits, local secret storage, and x402 paid-tool readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Echo Gate local-first agent-tool gateways, including tool registration, authenticated calls, key lifecycle operations, receipt checks, local health checks, and release readiness tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports sensitive key operations, including API key creation, listing, revocation, and policy changes. <br>
Mitigation: Approve key creation, revocation, and policy changes deliberately, and keep ECHO_GATE_ADMIN_TOKEN and egk_ API keys out of chat, commits, docs, and memory. <br>
Risk: The skill may guide remote deployment or paid-tool preparation actions. <br>
Mitigation: Review the external npm package before global installation and explicitly approve remote deployment or paid-tool preparation steps before execution. <br>


## Reference(s): <br>
- [Echo Gate ClawHub release page](https://clawhub.ai/builtbyecho/echo-gate) <br>
- [Declared Echo Gate GitHub project](https://github.com/BuiltByEcho/echo-gate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference sensitive credentials such as ECHO_GATE_ADMIN_TOKEN and egk_ API keys; users should keep those values out of chat, commits, docs, and memory.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
