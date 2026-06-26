## Description: <br>
Integrate Didit Face Match standalone API to compare two facial images, return a similarity score from 0 to 100, and support configurable thresholds, image rotation, and multi-face detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and identity-verification teams use this skill to compare a user's face image with a reference image through Didit's Face Match API. It helps implement biometric comparison workflows such as selfie-to-document matching while returning status, score, warnings, and face metadata for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images are biometric data and are sent to Didit for comparison. <br>
Mitigation: Use the skill only with clear consent from the people in the images and review Didit's retention settings before deployment. <br>
Risk: The API key grants access to Didit services. <br>
Mitigation: Store DIDIT_API_KEY in a protected secret store and avoid exposing it in logs, scripts, or shared configuration. <br>
Risk: Face match scores can be misused as the sole basis for high-stakes identity decisions. <br>
Mitigation: Treat the score as one signal, review warnings and thresholds, and add manual or policy review for high-impact use cases. <br>
Risk: Unnecessary vendor_data can increase privacy exposure. <br>
Mitigation: Send only the minimum vendor_data needed for operational tracking. <br>


## Reference(s): <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit Face Match API Reference](https://docs.didit.me/standalone-apis/face-match) <br>
- [Didit Face Match Feature Guide](https://docs.didit.me/core-technology/face-match/overview) <br>
- [Didit Business Console](https://business.didit.me) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with code examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY and sends user_image and ref_image files to Didit's Face Match API.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
