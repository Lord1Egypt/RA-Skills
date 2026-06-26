## Description: <br>
根据生命周期、风险偏好、投资目标和资产规模，生成资产配置、基金配置、定投和再平衡建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce educational asset-allocation plans, including risk assessment, lifecycle allocation ratios, periodic investment plans, and rebalancing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat educational allocation output as personalized financial, tax, or legal advice. <br>
Mitigation: Present outputs as educational guidance, avoid collecting unnecessary personal financial details, and independently verify investment and tax implications before acting. <br>
Risk: The optional Python calculator runs locally and may be executed without review. <br>
Mitigation: Review the script before running it and execute it only in an environment where local script execution is acceptable. <br>


## Reference(s): <br>
- [Allocation Theory](references/allocation-theory.md) <br>
- [Rebalance Calculator](calculators/rebalance-calculator.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lj22503/asset-allocator) <br>
- [Publisher Profile](https://clawhub.ai/user/lj22503) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with optional JSON-style structures, tables, formulas, and local Python calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces educational allocation and rebalancing content; it is not a substitute for professional financial, tax, or legal advice.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
