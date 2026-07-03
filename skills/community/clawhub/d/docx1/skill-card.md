## Description: <br>
Use this skill to create, read, edit, analyze, convert, and validate Word documents and DOCX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangxiaoqiang1992](https://clawhub.ai/user/yangxiaoqiang1992) <br>

### License/Terms of Use: <br>
Proprietary Anthropic terms <br>


## Use Case: <br>
Developers and document-focused agents use this skill to generate polished DOCX files, extract or reorganize Word content, manipulate comments and tracked changes, convert legacy Office files, and validate Office XML before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags the skill as suspicious because it can run external Office tooling and use native-code injection for LibreOffice in some environments. <br>
Mitigation: Install only after reviewing the LibreOffice shim behavior, and run conversion or tracked-change workflows in a controlled workspace. <br>
Risk: Office documents and converted files may contain untrusted content or unexpected document behavior. <br>
Mitigation: Use copies of documents, avoid untrusted Office files, and validate outputs before sharing or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangxiaoqiang1992/docx1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, XML snippets, and generated or modified Office files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke LibreOffice, pandoc, pdftoppm, npm docx tooling, and bundled Python utilities for Office file handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
