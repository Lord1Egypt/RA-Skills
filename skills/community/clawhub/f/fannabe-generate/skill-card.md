## Description:

Generate images, videos, and voice for your AI models via Fannabe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fannabe](https://clawhub.ai/user/fannabe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate and manage Fannabe image, video, voice, prompt, and gallery workflows from an agent by issuing CLI commands that spend the signed-in user's Fannabe credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap path installs a global, unpinned npm CLI.

Mitigation: Use a pinned Fannabe CLI version in a contained environment when reproducibility or supply-chain control matters.

Risk: Commands can use cached Fannabe credentials to spend credits or access account media.

Mitigation: Confirm estimated costs before non-trivial generation and use account or cost-preview commands before spending credits.

Risk: Image upload and prompt-from-image workflows can expose sensitive media or internal URLs to Fannabe services.

Mitigation: Avoid sensitive images, private media, and internal URLs in upload or from-image workflows unless the user explicitly approves.

## Reference(s):

- [Fannabe](https://www.fannabe.com)
- [Fannabe Generate on ClawHub](https://clawhub.ai/fannabe/skills/fannabe-generate)
- [Choosing an AI](references/ai.md)
- [Easy mode: Theme and Outfit presets](references/easy-mode.md)
- [Prompt assistance](references/prompt-tools.md)
- [Source media: image-to-video, edits, motion control, character swap](references/source-media.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may trigger asynchronous Fannabe jobs, downloads, account checks, uploads, and credit-spending generation through the signed-in user's account.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
