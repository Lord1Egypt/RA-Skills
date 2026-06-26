## Description: <br>
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
Proprietary. LICENSE.txt has complete terms <br>


## Use Case: <br>
Developers and agents use this skill to extract content from PDFs, generate or transform PDF documents, and complete PDF forms with field validation and visual review steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON, PNG, text, and PDF artifacts may contain private or sensitive document data. <br>
Mitigation: Use the skill only on PDFs the user is authorized to process, keep generated artifacts out of shared or synced locations when they contain private data, and delete intermediate files when finished. <br>
Risk: Decrypted, repaired, or filled PDFs can expose protected content or replace important document state. <br>
Mitigation: Work from a backup before repair or decryption steps, avoid in-place changes, and review generated PDFs before sharing or filing them. <br>


## Reference(s): <br>
- [PDF Processing Advanced Reference](reference.md) <br>
- [PDF Form Filling Workflow](forms.md) <br>
- [Adobe PDF 32000:2008 Standard](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce text extracts, JSON field maps, PNG validation images, and generated or filled PDF files during agent workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
