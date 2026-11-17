## Description:

用于创建、维护、版本化和质检本工作区的 BP 报告母版。适用于月报、季报、半年报、年报模板的结构维护、字段提示优化、BP 锚点一致性维护、BP 映射调整、版本升级判断，以及判断 BPMAP 文件和 BP 系统资料在母版维护中的使用边界。

This skill is ready for commercial/non-commercial use.

## Publisher:

[houtonghoutong](https://clawhub.ai/user/houtonghoutong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operators who maintain BP reporting templates use this skill to initialize, revise, version, and quality-check monthly, quarterly, half-year, and annual BP report master templates while preserving shared structure and BP anchors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify local BP report templates and version records in the target workspace.

Mitigation: Review proposed template and version-file changes before accepting them, especially when changes affect all reporting periods.

Risk: The bundled checker verifies template structure and fixed BP anchors, but it does not prove that a template matches every real BP instance.

Mitigation: Use the checker as a consistency aid and request explicit BP-system comparison only when a dedicated template adaptation review is needed.

## Reference(s):

- [资料优先级](references/source-priority.md)
- [BP系统资料使用说明](references/bp-system-sources.md)
- [模板规则](references/template-rules.md)
- [版本规则](references/versioning-rules.md)
- [BP系统API说明](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9FAPI%E8%AF%B4%E6%98%8E.md)
- [BP系统业务说明](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E8%AF%B4%E6%98%8E.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file edits and shell command recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or revise local BP template files, version-history files, and consistency-checking code in the target workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
