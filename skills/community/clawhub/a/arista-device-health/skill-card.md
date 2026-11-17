## Description:

Arista EOS device health check and triage procedure for troubleshooting Arista 7000, 7500, and 720X series switches across CPU, memory, interface, environment, agent, MLAG, and VXLAN/EVPN health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers, operators, and incident responders use this skill to guide Arista EOS health audits, post-change verification, incident triage, and capacity checks. It helps produce severity-classified findings with recommended actions for system, interface, environment, MLAG, VXLAN/EVPN, and EOS agent health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is labeled read-only, but security evidence says it includes an EOS agent restart step that changes device state.

Mitigation: Require explicit operator approval before any EOS agent restart, confirm the selected agent and blast radius, collect logs first, and follow normal network change-control procedures.

Risk: Health findings depend on accurate device context, expected baselines, and topology details supplied by the operator.

Mitigation: Validate outputs against current device data, known baselines, MLAG peer context, expected VTEP counts, and BGP EVPN peer lists before taking remediation action.

## Reference(s):

- [Arista EOS CLI Reference](artifact/references/cli-reference.md)
- [Arista EOS Threshold Tables](artifact/references/threshold-tables.md)
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/arista-device-health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with EOS CLI and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnostic findings, severity classifications, recommended actions, and a next-check cadence based on operator-provided device data.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
