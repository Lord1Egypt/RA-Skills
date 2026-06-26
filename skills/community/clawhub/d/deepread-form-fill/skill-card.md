## Description: <br>
AI-powered PDF form filling that accepts a PDF and JSON data, detects fields visually, maps values semantically, performs quality checks, and returns a completed PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to submit existing PDF forms and structured JSON data to DeepRead, then retrieve a filled PDF and quality report. It is suited for document workflows such as applications, claims, onboarding packets, and other PDF form automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs and JSON form data are sent to DeepRead's external service for processing. <br>
Mitigation: Use only when that data transfer is approved, and review DeepRead privacy, retention, and compliance terms before processing sensitive documents. <br>
Risk: API keys, signed download links, and webhook endpoints can expose submitted or completed documents if mishandled. <br>
Mitigation: Use a dedicated rotatable API key, keep signed URLs and webhook endpoints private, and rotate credentials if exposure is suspected. <br>
Risk: AI form filling may leave fields flagged for human review or produce values that need verification. <br>
Mitigation: Review the returned quality report and any human-in-the-loop flags before relying on completed forms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-form-fill) <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead dashboard](https://www.deepread.tech/dashboard) <br>
- [DeepRead BYOK setup](https://www.deepread.tech/dashboard/byok) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls] <br>
**Output Format:** [Markdown guidance with curl commands, Python and shell examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY; sends selected PDFs and JSON form data to DeepRead and returns a filled PDF URL plus a quality report.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
