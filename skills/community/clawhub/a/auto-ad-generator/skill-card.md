## Description:

Generates professional advertisement posters across industries using AI-generated or PIL backgrounds, product compositing, typography guidance, and platform-specific formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snakeruru](https://clawhub.ai/user/snakeruru)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing creators and agents use this skill to generate product advertisement poster workflows for automotive, tourism, fragrance, tea, recruiting, and public-welfare campaigns. It helps prepare layouts, prompts, compositing steps, and platform-specific outputs for WeChat, Xiaohongshu, airport displays, and lightboxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Dreamina installer uses a remote shell pipeline.

Mitigation: Independently verify and trust the Dreamina source before running the installer; prefer reviewed installation steps in controlled environments.

Risk: The skill can use paid or networked image-generation and background-removal services.

Mitigation: Run it with only the API keys and image files needed for the task, and confirm service cost and data-handling expectations before use.

Risk: Generated advertising assets may be misleading, off-brand, or unsuitable for regulated campaigns.

Mitigation: Review final posters, claims, logos, and celebrity or brand references before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snakeruru/skills/auto-ad-generator)
- [Dreamina CLI](https://jimeng.jianying.com/cli)
- [Li Auto Examples](references/li_auto_examples.md)
- [Color Palettes](references/color_palettes.json)
- [Typography Guide](references/typography_guide.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, image files]

**Output Format:** [Markdown guidance with inline bash commands and generated poster image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PIL and Dreamina backends, multiple platform aspect ratios, product-image compositing, and optional background removal.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
