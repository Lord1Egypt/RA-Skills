## Description: <br>
Analyzes scientific PDF figures by extracting images and text with PyMuPDF, using Kimi K2.6 vision analysis when available, and producing structured scientific interpretation and reverse-engineered visualization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjk1103](https://clawhub.ai/user/huangjk1103) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, research analysts, and scientific teams use this skill to extract figures from paper PDFs, combine figure captions with multimodal analysis, and produce structured knowledge about panels, measurements, trends, and likely visualization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted figures and prompts may be sent to Moonshot/Kimi for vision analysis. <br>
Mitigation: Use only approved PDFs, and avoid unpublished, confidential, regulated, patient, or proprietary content unless permission is clear. <br>
Risk: The workflow requires a sensitive MOONSHOT_API_KEY credential. <br>
Mitigation: Keep the key in an environment variable or secret manager and avoid hardcoding it in scripts, prompts, or shared documents. <br>


## Reference(s): <br>
- [Kimi K2.6 Vision API Reference](references/kimi-k2.6-vision-api.md) <br>
- [BusR Paper Case Study](references/busr-paper-case-study.md) <br>
- [Moonshot API Base](https://api.moonshot.cn/v1) <br>
- [Kimi Platform](https://platform.kimi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/huangjk1103/9cf703b) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style figure reports with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MOONSHOT_API_KEY for Kimi/Moonshot vision analysis when available and can fall back to text-only PDF extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
