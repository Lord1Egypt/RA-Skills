## Description: <br>
Skill Health Monitor helps agents audit skill collections for structure, content quality, maintenance activity, compatibility, and discoverability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review individual skills or collections, assign health scores, and identify maintenance work before skills degrade or fail silently. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit reports may expose local skill inventory details or git history. <br>
Mitigation: Review reports before sharing and remove sensitive repository, path, or history details. <br>
Risk: Checklist-based health scores can miss context-specific quality issues or overstate readiness. <br>
Mitigation: Treat scores as review guidance and confirm findings against the actual skill files before making release or retirement decisions. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aptratcn/aptratcn-skill-health-monitor) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown reports with checklist items and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local skill inventory details or git history when the agent follows the audit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
