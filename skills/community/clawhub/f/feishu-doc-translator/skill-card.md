## Description: <br>
飞书文档翻译助手在飞书文档之间进行中英文互译，支持全文翻译、段落翻译和双语对照。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[young-joey](https://clawhub.ai/user/young-joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to translate Feishu documents between Chinese and English, create bilingual versions, and preserve Markdown structure during document localization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translated output may be written to the source document or an existing document if the user selects that destination. <br>
Mitigation: Review the source document and destination before allowing writes, and prefer creating a new translated copy unless modifying an existing document is intentional. <br>
Risk: Confidential Feishu document content may be exposed according to the user's Feishu permissions and retention settings. <br>
Mitigation: Avoid using the skill on confidential documents unless the user's access permissions and retention expectations are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/young-joey/feishu-doc-translator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Translated Feishu document content with preserved Markdown structure and optional bilingual layout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a new translated document, append translated content below the source, or produce bilingual source-and-translation output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
