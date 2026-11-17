## Description:

An advanced AI agent that acts as a Senior Brand Strategist. It automates project setup, applies elite market methodologies (Archetypes, StoryBrand, Personas), and generates structured brand assets while preventing hallucinations via strict context shielding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vansearch](https://clawhub.ai/user/vansearch)

### License/Terms of Use:

MIT

## Use Case:

Brand strategists, designers, and marketing teams use this skill to initialize client branding workspaces, structure raw client intelligence, and generate strategic brand assets such as positioning, archetypes, personas, tone of voice, and Markdown-ready deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include an unsafe unpinned and mismatched NPX command.

Mitigation: Review install commands before execution; prefer the checked-in CLI directly or a pinned exact package name.

Risk: Branding projects may involve private client recordings, transcripts, PDFs, or briefs.

Mitigation: Use only authorized client materials and remove sensitive information before uploading or processing them with an agent.

Risk: The shipped package may provide scaffolding and reference guidance more than a complete autonomous strategist system.

Mitigation: Treat generated strategy as a draft and have a qualified reviewer check claims, positioning, and client fit before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vansearch/skills/flwr-branding-studio-kit)
- [README](README.md)
- [RACE framework](docs/race_framework.md)
- [Prompt guide template](docs/prompt_guide_template.md)
- [Branding glossary](docs/branding_glossary.md)
- [FLWR Branding Studio Instagram](https://instagram.com/flwr.branding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown strategy assets and setup guidance with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates client project folders and may copy Markdown templates when installed templates are present.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
