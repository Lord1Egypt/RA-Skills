## Description: <br>
Crosscomply Check helps agents answer cross-border e-commerce product compliance questions by mapping a product category and destination market to certification, labeling, packaging, testing, restriction, scoring, and next-action guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheyuy](https://clawhub.ai/user/sheyuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace operators, and support agents use this skill to triage export and marketplace compliance requirements for supported products and destination markets. It is a quick reference aid and should not replace current official requirements or professional legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance guidance can be incomplete or outdated for shipment, certification, customs, or marketplace decisions. <br>
Mitigation: Confirm the product category, destination market, and current official requirements before acting; consult qualified compliance or legal professionals for high-risk decisions. <br>
Risk: The skill covers a defined matrix of eight product categories and eight markets, so unsupported or edge-case products may receive overly broad guidance. <br>
Mitigation: Check that the request fits the documented coverage and treat unsupported categories or markets as requiring separate research and human review. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/Sheyuy/compliance-skills/tree/main/crosscomply_check) <br>
- [ClawHub skill page](https://clawhub.ai/sheyuy/crosscomply-check) <br>
- [Compliance data matrix](references/compliance-data.md) <br>
- [SkillHub online experience](https://skillhub.cn/skills/crosscomply-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured tables and optional JSON-style next-action fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses product category, destination country, optional existing compliances, brand status, and product value to produce compliance checklists, scores, warnings, and next actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
