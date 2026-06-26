## Description: <br>
This skill generates AI images from prompts through CreatOK's image generation API and can recover interrupted image generation tasks from an existing task ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newt0n](https://clawhub.ai/user/newt0n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images or product visuals from prompts, optionally with reference images, and to check or resume existing image generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, task IDs, generated image URLs, and optional reference images are sent to CreatOK and may be written to local artifacts. <br>
Mitigation: Use the skill only when you trust CreatOK for the supplied content, use a dedicated API key where possible, and delete local .artifacts outputs when task IDs or image URLs are sensitive. <br>
Risk: Image generation may consume credits or incur cost. <br>
Mitigation: Review the model, resolution, image count, and estimated credits before confirming generation; the skill includes a confirmation gate before submission. <br>
Risk: A missing or invalid CreatOK API key prevents the skill from running. <br>
Mitigation: Configure CREATOK_API_KEY before use and rotate the key if authorization errors occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newt0n/creatok-generate-image) <br>
- [CreatOK API keys](https://www.creatok.ai/app/workspace/api-keys) <br>
- [CreatOK agent skills](https://www.creatok.ai/agent-skills) <br>
- [Common CreatOK skill rules](references/common-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [User-facing text plus persisted result.json and result.md artifact files containing task status and generated image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns final image URLs verbatim when generation succeeds and records task IDs so interrupted runs can be recovered.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
