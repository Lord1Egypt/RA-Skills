## Description:

Content Claw turns papers, podcasts, case studies, and topical research into publish-ready social posts, infographics, diagrams, posters, captions, and related content assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to extract source material, create recipe-driven content specs, generate platform-ready social copy, and produce image assets for social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary source URLs during extraction.

Mitigation: Run extraction in a sandbox with restricted network access and avoid internal, sensitive, or untrusted URLs.

Risk: The skill can write generated files from user-controlled recipe, brand, and run names.

Mitigation: Validate recipe and brand names before allowing writes and keep file operations constrained to the skill workspace.

Risk: The Reddit agent is designed to make AI-written content read like organic human testimony.

Mitigation: Review, disable, or rewrite that agent for transparent, fact-backed drafts before deployment.

Risk: The skill depends on external services for image generation and topic discovery.

Mitigation: Use scoped, usage-limited API keys and review what condensed image specs or search queries are sent to each service.

## Reference(s):

- [Content Claw ClawHub Page](https://clawhub.ai/thierrypdamiba/skills/content-claw)
- [Content Claw Repository](https://github.com/scaleintelligence/content-claw)
- [Running Recipes](references/run-recipe.md)
- [Create Recipe Wizard](references/create-recipe.md)
- [Brand Graphs](references/brand.md)
- [Topic Discovery](references/topics.md)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Image files, YAML configuration, Shell commands, Guidance]

**Output Format:** [Markdown responses, JSON specs, YAML recipes and brand graphs, shell commands, and generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recipe runs may write generated specs, rendered text, images, and metadata under the skill content directory; image generation requires FAL_KEY and topic discovery requires EXA_API_KEY.]

## Skill Version(s):

3.3.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
