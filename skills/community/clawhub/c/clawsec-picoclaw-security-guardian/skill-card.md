## Description: <br>
Picoclaw security posture skill with advisory awareness, configuration drift detection, and supply-chain verification guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to review Picoclaw deployments for advisory exposure, configuration drift, and release artifact supply-chain verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for Picoclaw security review workflows and may not apply to general OpenClaw hook execution. <br>
Mitigation: Install and run it only for Picoclaw gateways or lightweight AI gateway deployments. <br>
Risk: Unsigned advisory modes can weaken recurring or production checks. <br>
Mitigation: Keep advisory feeds in verified mode and use unsigned modes only for short, documented emergency or offline windows. <br>
Risk: Profile generation reads local Picoclaw configuration and writes a report under the selected Picoclaw home. <br>
Mitigation: Run profile generation against the intended PICOCLAW_HOME and review the configured output path before use. <br>
Risk: Supply-chain verification depends on trusted manifests, signatures, and public keys. <br>
Mitigation: Require signed checksum manifest verification for passing supply-chain results and separately review third-party wrapper provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-picoclaw-security-guardian) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces on-demand local profile, drift, advisory, and supply-chain verification outputs for Picoclaw security review workflows.] <br>

## Skill Version(s): <br>
0.0.6 (source: server release metadata, SKILL.md frontmatter, skill.json, CHANGELOG.md released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
