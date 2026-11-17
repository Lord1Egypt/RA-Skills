## Description:

Extracts brand identity signals from a website URL, including colors, typography, visual style, imagery, and a structured brand profile for on-brand content generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and brand teams use this skill to analyze public websites and create reusable visual brand profiles before generating on-brand content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzing websites without authorization may create legal, privacy, or terms-of-service concerns.

Mitigation: Use the skill only on public sites you are allowed to analyze and review each target site's restrictions before scraping.

Risk: Images and derived brand metadata may be sent to Gemini or OpenAI for visual analysis.

Mitigation: Avoid sensitive or private targets, disclose external processing where required, and review provider data-handling terms before use.

Risk: A Supabase service-role key can grant broad database access if reused from a production project.

Mitigation: Keep caching disabled unless needed, use a scoped non-production key, and store secrets outside prompts, logs, and source files.

Risk: Installing scraping, browser, image-processing, and VLM dependencies expands the local execution surface.

Mitigation: Install dependencies in a virtual environment or container and review the package set before deployment.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/brand-dna-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks, plus structured brand profile data when implemented]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON-like BrandDNA objects containing colors, typography, imagery, visual style, cache status, and error fields.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
