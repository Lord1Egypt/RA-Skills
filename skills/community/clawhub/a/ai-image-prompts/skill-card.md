## Description:

Recommends curated, model-agnostic image generation prompts with sample images from a 10,000+ prompt library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and developers use this skill to find image prompt templates for portraits, product imagery, social media, posters, articles, videos, podcasts, and marketing content. The skill can recommend existing prompt examples and help customize a selected template for the user's content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact GitHub and YouMind, update local reference files, and download preview images from remote URLs.

Mitigation: Install only in environments where those network calls and local reference updates are acceptable; stricter deployments should review or disable auto-update and media-download behavior.

Risk: Reference prompt data is mutable and may change after installation.

Mitigation: Pin or verify the reference data source before use in controlled environments, and refresh only through reviewed update procedures.

Risk: Prompt recommendations may be incorrect, stale, or unsuitable for a user's image generation policy requirements.

Mitigation: Review generated recommendations and sample-image links before use, especially for brand, safety, legal, or regulated content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dophinl/skills/ai-image-prompts)
- [Prompt Gallery](https://youmind.com/nano-banana-pro-prompts)
- [Reference Data Source](https://github.com/YouMind-OpenLab/ai-image-prompts-skill/tree/main/references)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with prompt previews, links, sample image references, and inline shell commands when setup or media download steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are normally limited to up to three prompt templates, with English prompt content and user-language explanations.]

## Skill Version(s):

1.0.9 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
