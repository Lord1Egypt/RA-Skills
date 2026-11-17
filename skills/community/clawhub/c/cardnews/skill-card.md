## Description:

Generate Instagram-ready card news (카드뉴스) image sets from a topic, including slide planning, image generation prompts, PNG-to-JPG conversion, Korean captions, and upload preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Creators, marketers, and social media teams use this skill to turn a topic into a five-slide Korean Instagram carousel with consistent visual direction, caption text, JPG conversion, and upload preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can move from asset preparation toward live Instagram posting.

Mitigation: Review every generated slide and caption, and confirm the target Instagram account before any browser upload.

Risk: The artifact directs slide 5 to include penguin branding.

Mitigation: Remove or explicitly approve the branding before publishing the carousel.

Risk: The conversion script attempts to install Pillow automatically if it is missing.

Mitigation: Install Pillow in a controlled environment and review dependency installation before running the script.

Risk: Generated card-news content can contain factual or contextual mistakes.

Mitigation: Verify claims, examples, and captions before publishing.

## Reference(s):

- [Cardnews design guide](references/design-guide.md)
- [Cardnews ClawHub release page](https://clawhub.ai/mupengi-bot/skills/cardnews)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, image-generation prompts, JPG output files, and Korean caption text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans five square slides and converts PNG files to Instagram-ready JPG files at configurable size and quality.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
