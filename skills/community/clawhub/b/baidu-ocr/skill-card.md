## Description: <br>
Baidu Ocr uses the Baidu AI Open Platform OCR API to extract mixed Chinese and English text from images, with documented support for formula and table OCR workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run Baidu cloud OCR against local image files and return recognized text or JSON-formatted OCR results. It is suited to workflows that need OCR extraction from JPG, PNG, BMP, WEBP, or GIF inputs after Baidu OCR credentials and service permissions are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact embeds Baidu API credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed keys, and load least-privilege Baidu OCR credentials from secure configuration before use. <br>
Risk: Selected image files are uploaded to Baidu for OCR processing, and the artifact under-discloses that third-party data transfer. <br>
Mitigation: Warn users before processing, obtain appropriate approval for sensitive images, and avoid sending regulated or confidential data unless the Baidu service terms and organizational controls permit it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nidhov01/baidu-ocr) <br>
- [Baidu OCR Documentation](https://ai.baidu.com/ai-doc/OCR/Ek3h7xypm) <br>
- [Baidu API Reference](https://ai.baidu.com/ai-doc/REFERENCE/Wk3h7x8bv) <br>
- [Baidu OCR Product Page](https://ai.baidu.com/product/ocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text OCR lines or JSON-formatted OCR results, with Markdown setup and usage guidance in the artifact documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus Baidu API credentials and enabled OCR service permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
