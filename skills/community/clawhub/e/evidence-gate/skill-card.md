## Description: <br>
Generates evidence obligations for a claim or action, evaluates existing evidence against them, and returns a structured verdict with safe downgrade guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanicky](https://clawhub.ai/user/shanicky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to add an evidence gate before strong conclusions, root-cause diagnoses, safety assertions, or high-impact recommendations. It helps the caller define concrete evidence requirements, evaluate explicit evidence, and downgrade unsupported claims or actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may downgrade or block a claim when the invocation omits relevant evidence. <br>
Mitigation: Provide explicit evidence, alternatives checked, and any local policy requirements in the invocation; treat the verdict as gate guidance rather than domain expertise. <br>
Risk: The skill influences agent wording and recommendations around strong conclusions or risky actions. <br>
Mitigation: Review BLOCK, CONFLICT, and high-impact SOFT_PASS outputs before acting, and gather the targeted evidence checks it recommends. <br>


## Reference(s): <br>
- [Evidence Gate Protocol](references/protocol.md) <br>
- [Evidence Gate Input Template](references/input-template.md) <br>
- [Evidence Gate Output Template](references/output-template.md) <br>
- [Evidence Gate Verdict Schema](references/verdict-schema.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/shanicky/evidence-gate) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, guidance, json] <br>
**Output Format:** [JSON verdict object with evidence requirements, sufficiency assessment, allowed and blocked actions, fallback wording, and next evidence actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns PASS, SOFT_PASS, BLOCK, or CONFLICT and keeps evidence evaluation scoped to explicit artifacts supplied in the invocation.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
