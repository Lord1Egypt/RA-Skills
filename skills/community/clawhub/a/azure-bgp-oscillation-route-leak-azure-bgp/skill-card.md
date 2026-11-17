## Description:

Analyze and resolve BGP oscillation and BGP route leaks in Azure Virtual WAN-style hub-and-spoke topologies and similar cloud-managed BGP environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network engineers use this skill to analyze Azure Virtual WAN-style BGP instability, route leaks, preference cycles, and candidate mitigations. It helps distinguish allowed policy-level fixes from prohibited topology-disrupting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routing recommendations could be incorrect for a user's live Azure network topology or policy constraints.

Mitigation: Treat outputs as advisory and verify proposed changes against the user's network design, change-control process, and Azure documentation before applying them.

Risk: The skill discusses prohibited fixes such as disabling BGP, shutting down peering, removing connectivity, or restarting gateways.

Mitigation: Reject topology-disrupting fixes and prefer policy-level mitigations such as routing intent, export policy, communities, UDRs, and ingress filtering.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory routing guidance should be verified against the user's own network design and Azure documentation before policy changes are applied.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
