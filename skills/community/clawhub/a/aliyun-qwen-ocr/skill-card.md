## Description: <br>
Use when OCR-specialized extraction is needed with Alibaba Cloud Model Studio Qwen OCR models (`qwen-vl-ocr`, `qwen-vl-ocr-latest`, and snapshots), including document parsing, table parsing, multilingual OCR, formula recognition, and key information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare normalized Alibaba Cloud Model Studio Qwen OCR requests for document text extraction, table parsing, multilingual OCR, formula recognition, and key information extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document images, data URLs, prompts, and saved request files may contain sensitive or regulated information. <br>
Mitigation: Use the skill only when Alibaba Cloud OCR processing is appropriate, avoid unauthorized confidential documents, use limited-scope DashScope credentials, and delete or redirect saved request files that contain sensitive inputs. <br>


## Reference(s): <br>
- [Qwen OCR API Reference Notes](references/api_reference.md) <br>
- [Qwen OCR Source Links](references/sources.md) <br>
- [Qwen-OCR documentation](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr) <br>
- [Qwen-OCR API reference](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference) <br>
- [Model releases](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Model list](https://help.aliyun.com/zh/model-studio/models) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-qwen-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON request payload files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes normalized OCR request payloads to output/aliyun-qwen-ocr/request.json by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
