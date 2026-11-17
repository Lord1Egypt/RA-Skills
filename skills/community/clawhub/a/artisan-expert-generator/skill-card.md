## Description:

基于职业身份知识结构自动生成专家Skill；支持6维度采集、用户私有知识融合、框架提炼、质量验证与双Agent精炼。当用户需要创建职业专家助手、构建领域专业视角或生成标准化专业知识输出时使用此工具即可

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create standardized professional expert skills from a target occupation, optional private knowledge files, domain frameworks, ethics boundaries, and expression preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process private documents and include sensitive or regulated information in generated skill material.

Mitigation: Provide only documents intended for skill generation, avoid secrets or regulated data unless necessary, and review generated SKILL.md content before installing or sharing it.

Risk: The skill can write persistent files to user-selected paths, creating overwrite or misplaced-output risk.

Mitigation: Run it in a limited workspace, choose output paths carefully, and inspect generated files before use.

Risk: Generated professional guidance may be incorrect, stale, or affected by untrusted source material.

Mitigation: Review and scan every generated skill before deployment, and validate domain-specific claims against trusted professional sources.

## Reference(s):

- [6维度采集详细指南](references/collection-dimensions.md)
- [跨学科专家专项指南](references/cross-disciplinary-guide.md)
- [表达能力模块指南](references/expression-capabilities.md)
- [专业视角内核提取方法论](references/extraction-methodology.md)
- [互联网行业专项指南](references/internet-industry-guide.md)
- [知识融合方法指南](references/knowledge-fusion-methods.md)
- [职业身份分类参考](references/profession-taxonomy.md)
- [专家SKILL.md模板参考](references/skill-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files, JSON script responses, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can parse PDF, Word, Markdown, and text inputs; can write persistent SKILL.md files to user-selected output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
