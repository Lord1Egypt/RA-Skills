## Description: <br>
Analyze and resolve BGP oscillation and BGP route leaks in Azure Virtual WAN-style hub-and-spoke topologies and similar cloud-managed BGP environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network engineers use this skill to analyze Azure Virtual WAN-style hub-and-spoke BGP issues, identify oscillation or route-leak conditions from supplied topology and routing evidence, and select allowed policy-level mitigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing recommendations could be unsafe if topology, route-leak, or preference-cycle evidence is incomplete or inaccurate. <br>
Mitigation: Verify all topology and routing inputs before relying on the analysis. <br>
Risk: Suggested Azure routing policy, UDR, or export-filter changes could affect live traffic if applied without review. <br>
Mitigation: Have a qualified network operator review any proposed change before applying it to a live network. <br>
Risk: Sensitive network details or credentials could be exposed if included in prompts. <br>
Mitigation: Do not paste secrets into prompts, and redact sensitive operational data before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/wu-uk/azure-bgp-oscillation-route-leak-azure-bgp) <br>
- [Source skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown analysis with policy recommendations and fix classifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include explanations of preference cycles, valley-free violations, allowed mitigations, and rejected prohibited fixes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
