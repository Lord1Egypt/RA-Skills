## Description: <br>
Guide for uploading config.json, index.html, and preview.png to create and publish a mobile-compatible H5 touch game on the aigames repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianclan](https://clawhub.ai/user/brianclan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create and publish mobile-compatible H5 touch games by preparing config.json, index.html, and preview.png and uploading them to the external aigames service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to upload game files to a third-party service and make them available through a public URL. <br>
Mitigation: Review config.json, index.html, preview.png, and the game folder name before upload; do not upload private or proprietary files unless publication is intended. <br>
Risk: The upload interface does not overwrite existing files, so reused folder names or filenames can fail. <br>
Mitigation: Choose a unique English folder name and check upload responses before sharing the published game URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianclan/creategame) <br>
- [aigames repository service](https://www.idlab.top) <br>
- [Published game URL pattern](https://thenext.games/game/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for creating game assets and uploading them to a third-party service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
