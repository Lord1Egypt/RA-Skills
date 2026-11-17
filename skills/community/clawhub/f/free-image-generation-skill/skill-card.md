## Description:

Professional free image generation skill for agents. No API key required. Generate images from text with resilient retry/backoff and clean local file output. Supports free, high-volume usage patterns with responsible request pacing. Use when users request prompt-to-image generation or image bot automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrilaikram](https://clawhub.ai/user/mrilaikram)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate local image files from text prompts through a Perchance-based workflow without requiring an API key. It is suited for prompt-to-image generation and image bot automation where local file output and retry handling are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Perchance's unofficial image-generation service.

Mitigation: Use the skill only when external prompt processing is acceptable and avoid sending confidential or regulated content.

Risk: The generator can overwrite arbitrary user-writable files through the output path.

Mitigation: Run it with a dedicated output directory and avoid allowing untrusted users or automated workflows to choose the output path.

Risk: The setup script installs an unpinned dependency into the user Python environment.

Mitigation: Install dependencies in a virtual environment and pin dependency versions before deployment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/mrilaikram/skills/free-image-generation-skill)
- [Endpoint Notes](references/endpoints.md)
- [Integration Notes](references/telegram-delivery.md)
- [Perchance Image Generation API Endpoint](https://image-generation.perchance.org/api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; the generator script returns JSON and writes image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to the requested local output path; failures return structured error output.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
