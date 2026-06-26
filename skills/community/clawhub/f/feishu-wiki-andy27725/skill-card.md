## Description: <br>
Feishu knowledge base navigation for wiki spaces, wiki nodes, and wiki links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to navigate Feishu knowledge bases, inspect wiki node metadata, create or reorganize wiki pages, and coordinate wiki page content work through the required feishu_doc dependency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create wiki pages and move or rename wiki nodes in shared Feishu spaces. <br>
Mitigation: Prefer readonly Feishu permissions for browsing and require explicit confirmation before create, move, or rename actions. <br>
Risk: Wiki page content editing depends on the separate feishu_doc capability. <br>
Mitigation: Review and enable the feishu_doc dependency separately, and require explicit confirmation before writing document content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/feishu-wiki-andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires feishu_doc to read or edit wiki page document content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
