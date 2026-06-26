## Description: <br>
Detects and reads the largest license plate from a local image using the TrafficEye REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyedea-ai](https://clawhub.ai/user/eyedea-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run automatic number plate recognition on a local image through TrafficEye and receive the selected plate payload, including OCR text, type, dimensions, scores, unreadable status, and position. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle images and plate data are sent to an external TrafficEye service for recognition. <br>
Mitigation: Use the skill only for images you are authorized to process externally and confirm that TrafficEye handling is acceptable for the user's privacy and compliance requirements. <br>
Risk: API credentials can be exposed if passed through query-string authentication. <br>
Mitigation: Prefer header or bearer authentication and avoid query-string API keys when configuring the helper. <br>


## Reference(s): <br>
- [TrafficEye](https://trafficeye.ai) <br>
- [TrafficEye API](https://www.trafficeye.ai/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/eyedea-ai/automatic-number-plate-recognition) <br>
- [Publisher Profile](https://clawhub.ai/user/eyedea-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON plate-recognition payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path and TrafficEye API credentials; the helper selects the largest detected plate by polygon area.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
