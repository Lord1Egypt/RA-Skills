## Description: <br>
Extracts text, tables, and images from PDFs, including scanned PDFs, using the Mistral OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing teams use this skill to OCR PDFs or images, convert documents to Markdown and JSON, extract tables and images, and optionally return structured document fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs or images are sent to Mistral for OCR processing. <br>
Mitigation: Use only documents approved for transfer to Mistral, and avoid confidential or regulated files unless that transfer is authorized. <br>
Risk: OCR outputs and extracted assets are written to a local output folder. <br>
Mitigation: Choose an output directory that can be secured, reviewed, or cleaned up according to the document sensitivity. <br>
Risk: The workflow requires a Mistral API key. <br>
Mitigation: Store MISTRAL_API_KEY securely and avoid exposing it in logs, shell history, or shared configuration. <br>
Risk: Uploaded files may remain available to the Mistral service after OCR if not removed. <br>
Mitigation: Use the cleanup-upload option when local policy requires the script to attempt removal of uploaded files after processing. <br>


## Reference(s): <br>
- [Mistral OCR API quick reference](references/mistral_ocr_api.md) <br>
- [Output mapping rules](references/output_mapping.md) <br>
- [Document annotation prompts](references/annotation_prompts.md) <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/extracting-mistral-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON files with extracted image and table assets, plus shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include combined Markdown, per-page Markdown, raw OCR JSON, extracted images, extracted tables, and optional document annotation JSON or text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
