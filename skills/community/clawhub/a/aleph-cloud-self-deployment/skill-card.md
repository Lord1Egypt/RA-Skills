## Description: <br>
Autonomously provisions and configures an Aleph Cloud VM, installs OpenClaw, and prepares a spawned AI agent to operate on decentralized compute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[san-npm](https://clawhub.ai/user/san-npm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create and configure remote Aleph Cloud instances for OpenClaw agents. It is intended for workflows that require automated VM provisioning, agent runtime setup, credential placement, and follow-on self-deployment capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provision paid cloud infrastructure recursively through spawned remote agents. <br>
Mitigation: Require manual approval before each new VM, use budget alerts and low-balance accounts, and maintain a documented shutdown process. <br>
Risk: Aleph private keys and AI provider API keys may be copied to child VMs. <br>
Mitigation: Use delegated or per-instance keys where possible, avoid production secrets, restrict file permissions, and rotate any shared keys after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/san-npm/aleph-cloud-self-deployment) <br>
- [Aleph account portal](https://account.aleph.im/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, Python, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational setup steps for Aleph Cloud VMs, OpenClaw gateway configuration, credential handling, and shutdown guidance.] <br>

## Skill Version(s): <br>
1.0.2004 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
