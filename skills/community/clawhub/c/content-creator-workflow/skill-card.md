## Description:

Multi-modal content creation workflow for freelance creators that receives customer requests via WhatsApp, transcribes voice notes with the OpenAI Whisper API, generates images with DALL-E 3, and replies with the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Freelance creators and developers use this skill to automate request intake, audio transcription, prompt creation, image generation, and WhatsApp delivery for customer content requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores a WhatsApp messaging token in plaintext.

Mitigation: Use short-lived or test tokens, restrict permissions on ~/.wacli/config.json, or move the token to a secure secret store before handling real customer messages.

Risk: The workflow can automatically process customer content and reply with generated media.

Mitigation: Add consent and privacy notices for transcription and image generation, and require human review or policy checks before sending replies through a real WhatsApp backend.

## Reference(s):

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/content-creator-workflow)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with Python CLI commands; runtime scripts can produce transcript text files and generated PNG images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and OPENAI_API_KEY; generated files default to ./generated unless CONTENT_CREATOR_OUTPUT_DIR is set.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
