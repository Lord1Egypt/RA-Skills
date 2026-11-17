## Description:

FortiOS VDOM segmentation audit with UTM profile binding validation, FortiGuard service health assessment, SD-WAN security evaluation, and HA cluster posture check for FortiGate appliances and FortiGate-VM instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network security engineers, firewall administrators, and compliance reviewers use this skill to perform systematic FortiGate policy audits across VDOM segmentation, UTM coverage, FortiGuard health, SD-WAN steering, and HA posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may collect sensitive firewall configuration, policy, log, license, or topology information.

Mitigation: Run it only within an authorized audit scope and avoid sharing collected configs or logs outside that scope.

Risk: Some FortiOS commands used for runtime inspection or connectivity checks are operational rather than strictly passive.

Mitigation: Use least-privilege read-only or diagnose-level accounts and confirm before running log filters, pings, diagnostic filters, or REST API exports.

Risk: Audit conclusions depend on current FortiGate state and operator-provided topology expectations.

Mitigation: Validate findings against the active configuration, intended VDOM design, expected UTM policy, and approved SD-WAN or HA architecture.

## Reference(s):

- [FortiOS CLI Reference - Audit Commands](references/cli-reference.md)
- [FortiOS Policy Evaluation and VDOM Architecture](references/policy-model.md)
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/fortigate-firewall-audit)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with FortiOS CLI command blocks and audit report structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only audit procedures, finding criteria, remediation guidance, and report sections; does not include executable scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
