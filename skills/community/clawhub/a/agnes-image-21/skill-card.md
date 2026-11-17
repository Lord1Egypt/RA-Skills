## Description:

Generates and edits high-information-density images with Agnes Image 2.1 Flash, supporting text-to-image, image-to-image, multi-image composition, style transfer, and flexible image sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content creators use this skill to generate, edit, compose, and transform images through the Agnes API from prompts and public image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and the Agnes API key are sent to an external Agnes API.

Mitigation: Avoid confidential prompts and private or internal image URLs, and handle the API key as a secret environment variable.

Risk: The batch helper can run the wrong local executable from an untrusted working directory.

Mitigation: Run batch generation only from a trusted skill directory, or fix the helper to resolve the companion generator script relative to its own scripts directory before use.

## Reference(s):

- [API Documentation](artifact/references/API.md)
- [Prompt Guide](artifact/references/PROMPT_GUIDE.md)
- [Examples](artifact/references/EXAMPLES.md)
- [ClawHub Skill Page](https://clawhub.ai/lutongsuo/skills/agnes-image-21)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; script output is an image URL, image file, or Base64 text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANGES_API_KEY or AGENT_ANGES_API_KEY and sends prompts plus public image URLs to the Agnes API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
