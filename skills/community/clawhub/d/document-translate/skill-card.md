## Description: <br>
Doc Translate helps agents translate and localize PPTX, DOCX, XLSX, and PDF office documents while preserving templates and formatting where possible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lexyland](https://clawhub.ai/user/lexyland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to translate user-provided office documents, especially English-to-Chinese localization, and return translated files with the original layout preserved where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translated documents may contain sensitive or regulated information. <br>
Mitigation: Only process documents the user explicitly chooses, and confirm storage location, cleanup behavior, conversion tools, and any upload or sharing destination before using highly confidential files. <br>
Risk: Automatic translation mappings can mistranslate specialized terminology, brands, units, or formatting placeholders. <br>
Mitigation: Review translated files before relying on them and use curated terminology mappings for technical, medical, brand, numeric, unit, and placeholder-sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lexyland/document-translate) <br>
- [Skill workflow and format notes](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Translated document files plus Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports PPTX, DOCX, XLSX, and PDF; PDF conversion may create an intermediate DOCX and can require LibreOffice.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
