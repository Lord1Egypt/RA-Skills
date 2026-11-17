## Description:

Generate BNBOT lobster-bot mascot images in a consistent style using reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackleeio](https://clawhub.ai/user/jackleeio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate BNBOT-branded mascot artwork, stickers, social images, and character poses from approved style references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload prompts and reference images to Gemini using a Google AI API key.

Mitigation: Use a scoped API key, review prompts and reference images before generation, and avoid sending confidential or unapproved brand assets.

Risk: The script includes a hard-coded local .env fallback for API-key loading.

Mitigation: Remove the local path fallback and require credentials from the runtime environment or a managed secret store.

Risk: The script imports chromakey code from a neighboring skill outside this package.

Mitigation: Vendor, package, or pin that dependency so execution does not depend on mutable adjacent files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jackleeio/skills/bnbot-mascot)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [PNG image files with Markdown and Python or shell usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports transparent, black, or white backgrounds and named BNBOT reference poses.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
