## Description:

Generates and edits images with Gemini image models, including whiteboard-style diagrams, logo designs, and social media graphics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianyu110](https://clawhub.ai/user/xianyu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate or edit Gemini-based images for whiteboard diagrams, logos, and social media assets from prompts and optional source images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected source images, and API credentials may be sent to the configured Gemini endpoint, recommended third-party relay, or another custom relay.

Mitigation: Prefer the official Gemini endpoint, avoid unknown relays, use a separate revocable API key, and do not submit sensitive images or prompts.

Risk: The dependency declaration is lower-bounded rather than pinned, which can change runtime behavior over time.

Mitigation: Pin and review dependencies before deployment in controlled or commercial environments.

## Reference(s):

- [Bananapro Image Gen on ClawHub](https://clawhub.ai/xianyu110/skills/bananapro-image-gen)
- [Publisher profile: xianyu110](https://clawhub.ai/user/xianyu110)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [Gemini Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta)
- [Recommended relay endpoint](https://apipro.maynor1024.live/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image files when the bundled generation script is executed.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
