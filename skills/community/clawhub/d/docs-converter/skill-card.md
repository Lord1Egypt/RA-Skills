## Description: <br>
Converts PDFs, Office documents, and images through the wdangz.com API, including OCR and PDF merge, split, watermark, encryption, and decryption workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daizhenping012](https://clawhub.ai/user/daizhenping012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert non-sensitive PDF, Office, and image files, including OCR and PDF operations, through the wdangz.com API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to wdangz.com for conversion. <br>
Mitigation: Use the skill only for public or non-sensitive documents, and avoid contracts, IDs, financial records, credentials, regulated data, and confidential business files. <br>
Risk: The wrong local file or conversion operation could expose sensitive content to the external service. <br>
Mitigation: Confirm the exact file path and target operation before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daizhenping012/docs-converter) <br>
- [文档转换全能王](https://www.wdangz.com) <br>
- [wdangz conversion API endpoint](https://www.wdangz.com/api/v1/convert) <br>
- [wdangz status API endpoint](https://www.wdangz.com/api/v1/checkState) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Converted document files plus concise terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads converted files to the source file directory by default; requires WDANGZ_API_KEY and uploads selected files to wdangz.com.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
