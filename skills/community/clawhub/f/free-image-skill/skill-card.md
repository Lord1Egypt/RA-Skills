## Description:

Helps agents plan image workflows that combine OpenAI image generation, free stock-image search, watermark-removal tooling, and batch image optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[titancheung](https://clawhub.ai/user/titancheung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and publishing teams can use this skill to plan and run mixed image workflows for articles, reports, social posts, and other content assets. It provides commands and scripts for selecting AI-generated images, searching free stock sources, processing image files, and creating indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API quota or paid image-generation charges may occur despite zero-cost claims.

Mitigation: Use an isolated environment, review the scripts first, set provider-side spending limits, and prefer plan-only or dry-run modes before generation.

Risk: Watermark removal can violate license terms, creator rights, or platform rules.

Mitigation: Only remove watermarks from images you own or are explicitly allowed to modify, and keep source license and attribution records.

Risk: Stock-image license assumptions may be wrong for individual assets or providers.

Mitigation: Check each provider and asset license before commercial use, especially sources that require attribution.

Risk: The scripts perform network calls and local file operations.

Mitigation: Run the skill in a constrained workspace or virtual environment and review output directories before using generated assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/titancheung/skills/free-image-skill)
- [使用示例](artifact/references/使用示例.md)
- [图片解决方案项目](artifact/references/项目说明.md)
- [Demo README](artifact/examples/demo/README.md)
- [Unsplash](https://unsplash.com)
- [Pexels](https://www.pexels.com)
- [Pixabay](https://pixabay.com)
- [Freepik](https://www.freepik.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command examples, JSON indexes, and generated or processed image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use OPENAI_API_KEY, network access to image providers, local output directories, and ImageMagick for batch processing.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
