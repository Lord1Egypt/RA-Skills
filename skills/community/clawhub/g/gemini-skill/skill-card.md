## Description:

Gemini Skill automates Gemini website text Q&A and image generation through an OpenClaw browser profile, routing prompts by trigger phrases and returning answers or downloaded images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjz-p](https://clawhub.ai/user/wjz-p)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to ask Gemini a text question or generate images on Gemini from a prompt. The skill is intended for browser-based Gemini workflows that need explicit task routing, model selection, fallback handling, and returned answers or image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected prompts and generated images are sent to Gemini through the OpenClaw browser profile and may use a logged-in browser account.

Mitigation: Avoid sending secrets or sensitive personal data, and use an account and browser profile appropriate for the task.

Risk: Downloaded generated images may remain on local disk after the skill returns them.

Mitigation: Clean up downloaded images when they should not be retained.

## Reference(s):

- [Gemini](https://gemini.google.com)
- [Gemini Flow](references/gemini-flow.md)
- [Intent Routing](references/intent-routing.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown text with optional downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return one or more generated images in order; users receive progress guidance during image generation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
