## Description: <br>
基于职业身份知识结构自动生成专家Skill；支持6维度采集、用户私有知识融合、框架提炼、质量验证与双Agent精炼。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create structured professional expert skills from a target occupation, optional private documents, and preferred application scenarios. It guides collection, framework extraction, generated SKILL.md creation, validation, and optional refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python helper scripts parse selected documents and write generated files. <br>
Mitigation: Run the helpers only on files and output directories you intentionally choose, and inspect generated files before installation or sharing. <br>
Risk: Private documents used for expert generation may contain sensitive content. <br>
Mitigation: Prefer redacted or non-sensitive source documents, and avoid sending private document text to web search. <br>
Risk: Generated expert skills can contain incomplete, stale, or misleading professional guidance. <br>
Mitigation: Review the generated SKILL.md for domain accuracy, professional boundaries, and ethical limits before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ludiansheng/artisan-expert-generator) <br>
- [Collection Dimensions Guide](references/collection-dimensions.md) <br>
- [Cross-Disciplinary Guide](references/cross-disciplinary-guide.md) <br>
- [Expression Capabilities Guide](references/expression-capabilities.md) <br>
- [Extraction Methodology](references/extraction-methodology.md) <br>
- [Internet Industry Guide](references/internet-industry-guide.md) <br>
- [Knowledge Fusion Methods](references/knowledge-fusion-methods.md) <br>
- [Profession Taxonomy](references/profession-taxonomy.md) <br>
- [Skill Template Reference](references/skill-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON arguments and shell command examples; helper scripts can produce SKILL.md files and validation results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May parse user-selected PDF, Word, and Markdown files and write generated skill files to a user-specified output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
