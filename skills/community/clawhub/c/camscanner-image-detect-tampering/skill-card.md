## Description: <br>
CamScanner Detect Tampering helps an agent check whether a selected image appears edited, manipulated, or tampered with and report the returned conclusion to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camscanner-ai](https://clawhub.ai/user/camscanner-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to assess whether a photo or scanned image shows signs of editing or tampering. The agent uploads the selected image to CamScanner, reads the JSON result, and presents the boolean result and human-readable conclusion in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to CamScanner's servers for tampering analysis. <br>
Mitigation: Use the skill only when third-party image processing is acceptable, and avoid confidential documents, personal photos, or regulated data unless that processing has been approved. <br>
Risk: The service returns an automated tampering signal that may be incomplete or unsuitable as sole evidence. <br>
Mitigation: Present the result as the service's analysis and use additional review for high-impact authenticity decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/camscanner-ai/camscanner-image-detect-tampering) <br>
- [CamScanner homepage](https://www.camscanner.com) <br>
- [CamScanner AI tools service](https://ai-tools.camscanner.com) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/camscanner-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash examples and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects the agent to report is_tampered and result_text, translating the result text when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
