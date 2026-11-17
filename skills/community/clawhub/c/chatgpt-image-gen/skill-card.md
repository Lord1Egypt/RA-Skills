## Description:

Generate images using ChatGPT/DALL-E through OpenClaw browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonim1](https://clawhub.ai/user/sonim1)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to drive a logged-in ChatGPT browser tab for image generation requests and related download steps. It is intended for users who have intentionally attached OpenClaw browser control to their own ChatGPT session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs OpenClaw to control a logged-in ChatGPT browser session, so actions inherit the user's account permissions and settings.

Mitigation: Use it only when browser automation of the user's ChatGPT tab is intentional, review prompts before submission, and keep the relay attached only while needed.

Risk: The release security summary flags explicit bot-detection bypass framing around the browser relay workflow.

Mitigation: Prefer official or built-in image-generation paths when available and confirm that this automation approach is acceptable for the intended account and service context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonim1/skills/chatgpt-image-gen)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an attached Chrome or Brave browser tab with an active ChatGPT login.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
