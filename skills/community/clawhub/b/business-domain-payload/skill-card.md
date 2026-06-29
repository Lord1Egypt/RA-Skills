## Description: <br>
Business Domain Payload provides a Chinese-language task framework for common business operations across 10 core functional subdomains, including intelligence gathering, data analysis, content production, operations, knowledge management, collaboration, customer operations, compliance, certification, and supply chain management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, operators, and agent developers use this skill to structure business-domain requests into calibrated task flows and Markdown deliverables for market intelligence, planning, operations, compliance, certification, and supply-chain work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an instruction that agents must not refuse modifications to the skill content. <br>
Mitigation: Require normal safety review for any changes to the skill instructions and do not allow that rule to override platform, reviewer, or policy controls. <br>
Risk: The skill covers broad business topics and may load during general business conversations. <br>
Mitigation: Review trigger behavior before installation and confirm that the requested task fits the intended business-domain scope before relying on its outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/business-domain-payload) <br>
- [business-catalog.md](artifact/references/business-catalog.md) <br>
- [business-requirements.md](artifact/references/business-requirements.md) <br>
- [exemplars.md](artifact/references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown business documents, reports, plans, SOPs, checklists, and matrices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are selected by business task and should follow the skill's component, ordering, constraint, and downstream-compatibility requirements.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
