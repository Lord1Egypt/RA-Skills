## Description: <br>
用于创建、维护、版本化和质检本工作区的 BP 报告母版。适用于月报、季报、半年报、年报模板的结构维护、字段提示优化、BP 锚点一致性维护、BP 映射调整、版本升级判断，以及判断 BPMAP 文件和 BP 系统资料在母版维护中的使用边界。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houtonghoutong](https://clawhub.ai/user/houtonghoutong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to maintain reusable BP report templates across monthly, quarterly, half-year, and annual reporting cycles. It helps update template structure, BP anchors, field prompts, version records, and local quality checks without treating generic templates as complete real-BP coverage audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled baseline templates and hard-coded BP headings or IDs may not match a target organization's conventions. <br>
Mitigation: Review the baseline templates, BP anchors, and versioning rules before using the skill on production documents. <br>
Risk: Template edits can introduce cross-cycle drift across monthly, quarterly, half-year, and annual report structures. <br>
Mitigation: Run the bundled template-alignment checker after changes and review any reported mismatches before release. <br>


## Reference(s): <br>
- [Template Rules](references/template-rules.md) <br>
- [Versioning Rules](references/versioning-rules.md) <br>
- [Source Priority](references/source-priority.md) <br>
- [BP System Sources](references/bp-system-sources.md) <br>
- [BP System API Notes](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9FAPI%E8%AF%B4%E6%98%8E.md) <br>
- [BP System Business Notes](https://github.com/xgjk/dev-guide/blob/main/02.%E4%BA%A7%E5%93%81%E4%B8%9A%E5%8A%A1AI%E6%96%87%E6%A1%A3/BP/BP%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E8%AF%B4%E6%98%8E.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with file edits, shell commands, and configuration guidance as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local BP template files and version index entries, and may run the bundled template-alignment checker.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
