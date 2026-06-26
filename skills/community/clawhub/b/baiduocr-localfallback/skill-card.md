## Description: <br>
Provides Baidu OCR API access with EasyOCR local fallback, image preprocessing, token caching, and retry handling for text recognition from images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xx235300](https://clawhub.ai/user/xx235300) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and call Baidu OCR services for general text, cards, receipts, handwriting, tables, formulas, and other image-based recognition tasks, with local EasyOCR fallback when the remote service is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baidu OCR uploads can expose sensitive image contents to an external processor. <br>
Mitigation: Use local OCR for IDs, bank cards, passports, receipts, or other sensitive documents unless Baidu's data handling terms are acceptable for the use case. <br>
Risk: API credentials may be saved in a plaintext config file. <br>
Mitigation: Prefer environment variables for credentials, or restrict the config file permissions to the local user. <br>
Risk: The shell installer and dependencies can change the local Python environment and download OCR models. <br>
Mitigation: Review the installer source before execution and install in an isolated environment when possible. <br>


## Reference(s): <br>
- [Baidu Cloud OCR Documentation](https://cloud.baidu.com/doc/OCR/s/Ck3h7y2ia) <br>
- [ClawHub Skill Page](https://clawhub.ai/xx235300/baiduocr-localfallback) <br>
- [Publisher Profile](https://clawhub.ai/user/xx235300) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return OCR result JSON from Baidu OCR or EasyOCR fallback, including recognized words, locations, counts, and fallback metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
