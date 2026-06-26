## Description: <br>
FortiOS VDOM segmentation audit with UTM profile binding validation, FortiGuard service health assessment, SD-WAN security evaluation, and HA cluster posture check for FortiGate appliances and FortiGate-VM instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers and firewall administrators use this skill to audit FortiGate/FortiOS deployments for VDOM segmentation, UTM profile coverage, FortiGuard health, SD-WAN fail-open behavior, and HA posture during post-change, compliance, or baseline reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FortiGate audit output can expose sensitive configuration, topology, license, and security posture details. <br>
Mitigation: Run the skill only when authorized, use a least-privilege FortiOS account, and handle raw CLI output as sensitive security data. <br>
Risk: Some diagnostics, including ping and FortiGuard rating checks, are operational checks rather than purely passive reads. <br>
Mitigation: Review commands before execution, avoid unattended command execution, and get approval before running active diagnostics. <br>


## Reference(s): <br>
- [FortiOS Policy Evaluation and VDOM Architecture](references/policy-model.md) <br>
- [FortiOS CLI Reference - Audit Commands](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with FortiOS CLI command blocks and audit report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized read-only SSH access to FortiOS devices; raw CLI output can contain sensitive security data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
