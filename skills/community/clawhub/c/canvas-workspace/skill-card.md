## Description: <br>
Canvas Workspace helps agents generate or edit images, push images into a local canvas, inspect canvas state, and handle canvas marker files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quanming1](https://clawhub.ai/user/quanming1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to run a local canvas workspace, generate or edit images with configured providers, and send image outputs or existing URLs to the canvas for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches unpinned remote code with npx. <br>
Mitigation: Install only when the npm package is trusted and prefer pinning or reviewing the package version before use. <br>
Risk: The setup flow stores API keys persistently. <br>
Mitigation: Set API keys yourself in a scoped or temporary secret store and avoid committing or sharing shell profile changes. <br>
Risk: Image generation and editing can send prompts and image URLs to Qwen or Gemini endpoints. <br>
Mitigation: Do not provide private, confidential, or internal image URLs unless the selected provider is approved for that data. <br>
Risk: The canvas API reference documents a reset endpoint that can clear canvas data. <br>
Mitigation: Require explicit user confirmation before calling any reset endpoint. <br>


## Reference(s): <br>
- [Canvas API Reference](references/canvas-api.md) <br>
- [Canvas Workspace on ClawHub](https://clawhub.ai/quanming1/canvas-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local canvas APIs and configured external image-generation APIs.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
