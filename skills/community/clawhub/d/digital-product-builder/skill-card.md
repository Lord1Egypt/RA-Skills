## Description:

Digital Product Builder helps agents build and launch low-cost digital products for Gumroad, itch.io, and DriveThruRPG using Pillow for images and Groq for listing copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabroo3-commits](https://clawhub.ai/user/sabroo3-commits)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to produce digital product assets, listing copy, ZIP bundles, and storefront setup guidance for Gumroad, itch.io, and DriveThruRPG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Pillow without a pinned version can introduce dependency drift or unexpected package behavior.

Mitigation: Use a virtual environment and pin Pillow to a reviewed version before running image-generation snippets.

Risk: Storing a Groq API key in a persistent plaintext workspace file can expose credentials.

Mitigation: Prefer a session-scoped environment variable or a secret manager, and avoid committing or sharing files that contain API keys.

Risk: Prompts and listing copy sent to Groq may include sensitive, proprietary, customer, or licensed content.

Mitigation: Send only content that the user is comfortable having processed by Groq, and exclude secrets or unpublished proprietary material.

## Reference(s):

- [Digital Product Builder on ClawHub](https://clawhub.ai/sabroo3-commits/skills/digital-product-builder)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated listing copy, image-generation snippets, ZIP packaging instructions, and platform-specific publishing guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
