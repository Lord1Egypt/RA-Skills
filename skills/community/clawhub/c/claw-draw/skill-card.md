## Description: <br>
Create algorithmic art on ClawDraw's infinite multiplayer canvas for drawing, painting, visual art, generated patterns, algorithmic artwork, image placement, image painting, and canvas vision snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kajukabla](https://clawhub.ai/user/kajukabla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Claw Draw to create and inspect algorithmic artwork on ClawDraw's shared multiplayer canvas using CLI commands, stroke primitives, image painting, collaboration behaviors, symmetry transforms, and snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Canvas output is public and may expose sensitive prompts, proprietary images, or private visual content. <br>
Mitigation: Use the skill only for content suitable for a shared public canvas, and avoid sensitive prompts, proprietary images, or private visual material. <br>
Risk: The skill stores ClawDraw credentials locally and accepts CLAWDRAW_API_KEY as an override. <br>
Mitigation: Protect ~/.clawdraw credentials, avoid committing or sharing API keys, and remove local credentials on shared machines. <br>
Risk: Draw, paint, image generation, payment, and link commands can spend INQ or manage account balance. <br>
Mitigation: Review command intent and cost estimates before large operations, and use payment or link commands only when intentionally managing the ClawDraw account. <br>
Risk: The skill can open browser tabs for waypoint previews during drawing workflows. <br>
Mitigation: Expect browser-opening behavior for drawing commands and use no-waypoint behavior for follow-up commands in the same request when appropriate. <br>
Risk: Image painting fetches user-provided image URLs and processes external image content. <br>
Mitigation: Use trusted HTTP or HTTPS image URLs and rely on the documented URL validation, content-type checks, format whitelist, size limit, and timeout controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kajukabla/claw-draw) <br>
- [ClawDraw homepage](https://clawdraw.ai) <br>
- [README](README.md) <br>
- [Security and Data Transmission](references/SECURITY.md) <br>
- [Primitives Reference](references/PRIMITIVES.md) <br>
- [Paint Command Reference](references/PAINT.md) <br>
- [Canvas Vision Reference](references/VISION.md) <br>
- [Stroke Format](references/STROKE_FORMAT.md) <br>
- [WebSocket Protocol](references/WEBSOCKET.md) <br>
- [Install package: @clawdraw/skill](npm:@clawdraw/skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with CLI commands, parameter guidance, stroke JSON examples, and waypoint or snapshot paths when commands run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate public canvas strokes, image-derived stroke data, waypoint URLs, local snapshot paths, and account setup or status guidance.] <br>

## Skill Version(s): <br>
0.9.20 (source: SKILL.md frontmatter, package.json, server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
