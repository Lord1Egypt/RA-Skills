## Description:

Generate or edit images using Google's "Nano Banana" image models when a user explicitly asks for Gemini or Nano Banana image generation, iterative image edits, or reference-image composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or edit images through a local Nano Banana CLI backed by Google's Gemini image models, including prompt-only generation and edits that use one or more reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package relies on a separate home-directory CLI implementation that is not included in the artifact.

Mitigation: Install only after verifying the target of ~/bin/nano-banana, who can modify it, and what code it runs.

Risk: The external CLI receives the user's Gemini API key, prompts, and reference images.

Mitigation: Store the API key in a restricted credentials file, avoid logging or echoing secrets, and only send prompts or images that are acceptable for the Gemini service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyagil/skills/dyagil-nano-banana)
- [Google AI Studio API key page](https://aistudio.google.com/apikey)
- [Gemini generateContent API endpoint](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY})

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown with shell commands, generated image file paths, and MEDIA path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are written as PNG files by an external local CLI; model, aspect ratio, output path, output directory, reference images, and image count can be selected with CLI flags.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
