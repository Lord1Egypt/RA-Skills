## Description: <br>
Analyzes underwater coral reef images with YOLOv11 and MobileSAM to segment coral colonies, calculate coral coverage, and report detected colonies through the OpenClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingzhuangwang](https://clawhub.ai/user/mingzhuangwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marine ecologists, environmental agencies, and developers use this skill to submit reef images for coral colony segmentation, coverage percentage calculation, and colony detection counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads user-selected coral imagery to the OpenClaw API for analysis. <br>
Mitigation: Confirm the endpoint and publisher before use, use a scoped OpenClaw token when available, and avoid uploading sensitive imagery unless the service terms are acceptable. <br>
Risk: The skill is paid per invocation. <br>
Mitigation: Confirm expected usage and billing controls before running repeated or automated calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mingzhuangwang/coral-precise-coverage-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/mingzhuangwang) <br>
- [OpenClaw Coral API Endpoint](https://api.openclaw.io/v1/skills/coral-precise-coverage-ai/predict) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Files, Guidance] <br>
**Output Format:** [JSON response with coral coverage metrics and detected boxes, plus an optional decoded result image file and integration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid OpenClaw token and a user-selected JPEG or PNG image; invocations are paid through OpenClaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
