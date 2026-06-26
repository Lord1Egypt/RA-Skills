## Description: <br>
Translate files (PDF, DOCX, PPTX) to any language using the Bluente Translation API by collecting an API key, source files, target language, and output location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[varSmallRookie](https://clawhub.ai/user/varSmallRookie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users translate documents through the Bluente Translation API by providing a Bluente API key, source path, target language, and output path. The skill is useful when an agent should prepare and run the translation workflow and report where translated files were saved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are sent to the external Bluente Translation API. <br>
Mitigation: Use the skill only for documents approved for Bluente processing, especially for business, legal, medical, client, or regulated data. <br>
Risk: The workflow requires a Bluente API key. <br>
Mitigation: Provide the key only when needed and keep it out of shared logs, scripts, and source control. <br>


## Reference(s): <br>
- [Bluente Documentation](https://www.bluente.com/docs) <br>
- [Bluente Translation API](https://api.bluente.com/api/20250924/blu_translate) <br>
- [ClawHub Skill Page](https://clawhub.ai/varSmallRookie/bluente-translate) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, files, markdown, guidance] <br>
**Output Format:** [Markdown summary with generated Python code, shell execution output, and translated document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Bluente API key and sends selected documents to Bluente for translation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
