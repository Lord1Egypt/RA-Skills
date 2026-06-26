## Description: <br>
Face Transform helps agents use AceDataCloud Face APIs to analyze face keypoints, beautify portraits, age or gender transform faces, swap faces, create cartoon avatars, and detect liveness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare authenticated AceDataCloud Face API requests for face analysis and transformation workflows on authorized images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends face images to an external API and may process sensitive biometric data. <br>
Mitigation: Use only authorized images, obtain consent from depicted people, and confirm AceDataCloud privacy, retention, and data handling terms before using real face images or sensitive datasets. <br>
Risk: The skill supports identity-changing edits such as face swap, age change, gender change, and cartoon avatar generation. <br>
Mitigation: Restrict use to legitimate workflows and avoid deceptive, non-consensual, or harmful face edits. <br>
Risk: The artifact states the APIs are in Alpha stage and interfaces may evolve. <br>
Mitigation: Validate endpoint parameters and expected responses before relying on the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub Face Transform release](https://clawhub.ai/Germey/acedatacloud-face-transform) <br>
- [AceDataCloud Face Analyze API endpoint](https://api.acedata.cloud/face/analyze) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AceDataCloud API endpoints and requires ACEDATACLOUD_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
