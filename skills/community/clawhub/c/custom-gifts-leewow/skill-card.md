## Description: <br>
Leewow Custom Gifts lets an agent browse customizable products, upload a workspace image, generate an AI product mockup, download preview images, and provide a signed purchase link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yqxu](https://clawhub.ai/user/yqxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse custom gift templates, turn a user-provided image into a product preview, and share the resulting preview image and purchase link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user images to external Leewow and Tencent COS services. <br>
Mitigation: Use only images that are acceptable to share with those services and avoid sensitive files in the workspace. <br>
Risk: The skill relies on a Leewow secret key and produces signed purchase or COS URLs. <br>
Mitigation: Use a narrowly scoped Leewow key, never expose or log CLAW_SK, and treat signed URLs as temporary access credentials. <br>
Risk: The security review flags broad local configuration, URL-signing, shell-command, and endpoint surfaces. <br>
Mitigation: Review the skill before installing, avoid untrusted tool inputs, and constrain command templating, environment loading, endpoint allowlisting, and COS presigning before higher-trust use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yqxu/custom-gifts-leewow) <br>
- [Publisher Profile](https://clawhub.ai/user/yqxu) <br>
- [Leewow Service](https://leewow.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [JSON tool results, local image files, signed URLs, and Markdown or text guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads template and preview images under ~/.openclaw/workspace and requires CLAW_SK plus Leewow/Tencent COS access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
