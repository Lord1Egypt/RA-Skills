## Description:

EIGRP DUAL algorithm analysis with successor/feasible successor evaluation, stuck-in-active diagnosis, K-value validation, and redistribution loop detection for Cisco IOS-XE and NX-OS classic and named EIGRP modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill to troubleshoot Cisco EIGRP behavior, including missing routes, neighbor instability, stuck-in-active events, K-value mismatches, metric issues, and redistribution loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for authorized EIGRP troubleshooting and may involve routing tables, neighbor data, and running-configuration excerpts that are sensitive operational data.

Mitigation: Use it only on authorized Cisco environments, prefer read-only device credentials, and handle collected command output according to the organization's security controls.

Risk: Diagnostic recommendations can affect production routing if translated directly into configuration changes without review.

Mitigation: Validate findings against the current topology, platform mode, and change-control process before applying any remediation.

## Reference(s):

- [EIGRP CLI Reference - IOS-XE / NX-OS](references/cli-reference.md)
- [EIGRP DUAL Finite State Machine](references/state-machine.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic guidance with Cisco IOS-XE and NX-OS command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only guidance; the skill proposes diagnostic commands and analysis but does not execute commands itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
