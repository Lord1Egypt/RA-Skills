## Description: <br>
Deep Research to PPT Pro guides an agent through generating a sourced research report, converting it into a slide outline, producing slide images with Gemini, checking slide text with OCR, and assembling PPTX/PDF outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn a user-supplied research topic into a structured research report, slide outline, image prompts, generated slide images, and assembled presentation files. It is intended for workflows that can provide the required research and image-generation credentials and review generated content before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may attempt privileged system package installation for OCR dependencies. <br>
Mitigation: Review scripts before installation, run in a container or disposable environment, and install OCR dependencies manually on sensitive machines. <br>
Risk: The full workflow requires ZeeLin and Gemini API credentials and may send research topics or content to those providers. <br>
Mitigation: Use scoped, revocable keys, keep credential files out of version control, and avoid confidential topics unless provider sharing is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kelcey2023/desearch-ppt) <br>
- [Publisher profile](https://clawhub.ai/user/kelcey2023) <br>
- [PPT structure and outline guide](references/slide_structure.md) <br>
- [ZeeLin API key registration](https://desearch.zeelin.cn/skill-activity) <br>
- [Tesseract OCR Windows installer reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSON outlines/prompts, generated images, PPTX/PDF files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and GEMINI_API_KEY for the full workflow; OCR and presentation assembly depend on Python packages and Tesseract.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
