## Description:

Guides agents to use the Beauty Diagram CLI to generate, beautify, export, share, and embed Mermaid or PlantUML diagrams as polished SVG or PNG outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levi840714](https://clawhub.ai/user/levi840714)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agents use this skill to turn Mermaid or PlantUML source into presentation-ready diagram files, share links, or Markdown embeds. It also guides optional text-to-diagram generation through the Beauty Diagram CLI when the user has the required plan and API scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts invoke an unpinned npm CLI, so behavior could change when `npx @beauty-diagram/cli` resolves a newer package.

Mitigation: Pin or lock the `@beauty-diagram/cli` version before use and review package updates before adopting them.

Risk: Share and share-embed workflows can publish diagrams to public external URLs.

Mitigation: Ask for explicit approval before creating hosted URLs, and prefer local sidecar SVG output for private repositories or sensitive diagrams.

Risk: Diagram sources or prompts are sent to Beauty Diagram when workflows call the public API.

Mitigation: Use the skill only with content suitable for Beauty Diagram processing and run the CLI with least privilege in workspaces that may contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/levi840714/skills/beauty-diagram)
- [Beauty Diagram site](https://www.beauty-diagram.com)
- [Beauty Diagram CLI on npm](https://www.npmjs.com/package/@beauty-diagram/cli)
- [Beauty Diagram API keys](https://www.beauty-diagram.com/account/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Mermaid or PlantUML source, file paths, and generated SVG/PNG or share/embed URL references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local .mmd, .puml, .svg, or .png files and public Beauty Diagram share/embed URLs depending on the selected workflow.]

## Skill Version(s):

1.7.0 (source: ClawHub release, SKILL.md frontmatter, package.json; CHANGELOG top entry is 1.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
