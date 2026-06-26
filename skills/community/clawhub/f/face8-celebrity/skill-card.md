## Description: <br>
Upload a photo to identify celebrities using Face8 Taiwan face recognition engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichendong](https://clawhub.ai/user/ichendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit local photos to Face8 for celebrity or public-figure face recognition, with optional commands to register unknown faces or confirm suggested matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected photos are uploaded to face8.ai for face-recognition processing. <br>
Mitigation: Use only photos you are authorized to submit and avoid private individuals or photos without consent. <br>
Risk: The register and confirm options may make persistent changes to Face8's remote face database. <br>
Mitigation: Review intent before using --register or --confirm and limit those options to appropriate celebrity or public-figure records. <br>
Risk: Face8 recognition accuracy is not guaranteed. <br>
Mitigation: Treat matches and confidence scores as suggestions that need human review before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ichendong/face8-celebrity) <br>
- [Face8 FaceMaster](https://face8.ai/faceMaster/) <br>
- [Face8 FaceMaster API](https://face8.ai/faceMaster/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text recognition summaries or raw JSON API responses from a command-line Python script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include matched names, confidence percentages, face tokens, suggested alternatives, registration status, and confirmation status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
