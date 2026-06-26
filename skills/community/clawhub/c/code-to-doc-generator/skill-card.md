## Description: <br>
从代码和 UI 逆向提取业务逻辑，生成不同类型的项目文档，包括 BRD/MRD、PRD、HLD、DDD、LLD、编码指南、测试文档、运营手册、SLI/SLO 监控文档和 CI/CD 文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suifei](https://clawhub.ai/user/suifei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, product managers, QA engineers, SREs, DevOps teams, and operations staff use this skill to generate or synchronize project documentation from source code, UI text, and existing docs. It supports new documentation and reverse-sync workflows where code is treated as the source of truth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read project source, existing documentation, and sensitive local context while generating documentation. <br>
Mitigation: Run it only in the intended repository scope and avoid exposing secrets or unrelated files. <br>
Risk: Generated or synchronized documentation may introduce inaccurate guidance if code-derived facts and inferred statements are not reviewed. <br>
Mitigation: Review generated diffs before committing and verify any FACT, INFER, or OBSERVE annotations against the project. <br>
Risk: The artifact includes SVG content that may have interactive behavior in permissive viewers. <br>
Mitigation: Treat the SVG as inert content or disable its click handlers when viewing or publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suifei/code-to-doc-generator) <br>
- [Document Types Strategy](references/document-types.md) <br>
- [Document Structure Guide](references/document-structure.md) <br>
- [Analysis Dimensions](references/analysis-dimensions.md) <br>
- [Exploration Strategy](references/exploration-strategy.md) <br>
- [Reverse Sync Procedure](references/reverse-sync.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown documentation, Mermaid diagrams, structured summaries, and repository documentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update docs/[project]/ markdown files and OBSERVATIONS.md during reverse-sync workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
