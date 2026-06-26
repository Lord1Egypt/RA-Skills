## Description: <br>
Batch ID uses Tencent Cloud OCR to extract names, sex, and ID numbers from up to 50 ID-card images and return a formatted text file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyao58](https://clawhub.ai/user/linyao58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to process authorized batches of ID-card images through Tencent Cloud OCR and receive a downloadable, consistently formatted text result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes full government-ID data in bulk. <br>
Mitigation: Use it only for IDs the operator is authorized to process, with consent and compliance checks for Tencent Cloud OCR. <br>
Risk: The generated .txt attachment can expose sensitive identity data. <br>
Mitigation: Treat the output as highly sensitive, define retention controls, and consider masking ID numbers or avoiding plaintext export. <br>
Risk: Tencent Cloud credentials are required to call the OCR API. <br>
Mitigation: Use a dedicated least-privilege Tencent key and keep credentials in the skill configuration rather than source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linyao58/batch-id-ocr-to-txt) <br>
- [Tencent Cloud CAM API key console](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text file plus short status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts up to 50 image URLs and returns a generated .txt attachment containing extracted fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
