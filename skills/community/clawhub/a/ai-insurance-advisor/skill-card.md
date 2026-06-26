## Description: <br>
Chinese-language insurance planning assistant for mainland China insurance needs, including coverage-gap analysis, product comparison, premium estimates, compliance prompts, claims questions, social copy, and agent training scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mnetfairy](https://clawhub.ai/user/mnetfairy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in mainland China and insurance sales-support agents use this skill to analyze household protection needs, compare local insurance products, estimate premiums, and draft Chinese-language planning or sales-support material. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Insurance product availability, terms, and premiums can change after the local product database was generated. <br>
Mitigation: Verify product status, policy terms, and premium calculations with official insurers or licensed sources before making decisions. <br>
Risk: The skill may request sensitive personal, family, mortgage, income, health, and insurance information to produce suggestions. <br>
Mitigation: Collect only information needed for the current planning task, obtain user consent, and avoid storing or sharing personal data unless authorized. <br>
Risk: Sales-oriented recommendations or contact prompts can bias a user toward a specific sales channel. <br>
Mitigation: Present sales contacts transparently, respect opt-out, and encourage comparison through licensed providers that can evaluate products from multiple insurers. <br>
Risk: Planning, underwriting, claims, and compliance outputs may be incomplete or unsuitable for a user's legal or insurance situation. <br>
Mitigation: Treat outputs as general planning and sales-support material, and have licensed insurance or legal professionals review high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mnetfairy/skills/ai-insurance-advisor) <br>
- [Product database](references/products.json) <br>
- [Insurance knowledge base](references/insurance-knowledge.md) <br>
- [Compliance reference](references/compliance.md) <br>
- [Product data validation report](references/validation_report_20260524_090219.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Chinese-language Markdown and text, with JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts accept JSON input through stdin and emit JSON to stdout; user-facing responses are intended to be in Chinese.] <br>

## Skill Version(s): <br>
1.8.291 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
