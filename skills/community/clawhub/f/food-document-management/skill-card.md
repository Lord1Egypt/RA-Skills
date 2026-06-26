## Description: <br>
文档管理能力；支持研发文档分类、版本管理、模板生成；当进行研发资料整理或文档编写时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudyxuq](https://clawhub.ai/user/cloudyxuq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Food R&D teams and documentation staff use this skill to classify research documents, manage version records, generate reusable templates, and organize local document indexes for trials, process records, and related reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web searches for document standards may expose confidential project context if users add sensitive details to queries. <br>
Mitigation: Use generic search terms for external research and keep confidential product, formulation, customer, or project details out of web searches. <br>
Risk: Document metadata may be saved locally in data/docs/document_index.json when the helper script is used. <br>
Mitigation: Run the skill in an appropriate workspace, control access to generated local files, and avoid storing secrets or unnecessary confidential details in document metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudyxuq/food-document-management) <br>
- [R&D document classification standard](references/document_classification.md) <br>
- [Document templates overview](assets/templates/README.md) <br>
- [Trial report template](assets/templates/trial_report.md) <br>
- [Process record template](assets/templates/process_record.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with suggested web_search commands, document templates, and local index records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local document metadata under data/docs/ when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
