## Description:

Generates 1080x1350 news-style social media images with Thai text overlays and matching captions for Facebook and Instagram content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mewic](https://clawhub.ai/user/mewic)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content agents use this skill to create Thai-language news-style social posts with a generated JPEG image and matching caption text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install operating-system packages and fonts, including privileged writes to system font directories.

Mitigation: Run setup in a container or disposable workspace and avoid elevated privileges unless system package and font changes are acceptable.

Risk: The generator can load background images from arbitrary URLs.

Mitigation: Use trusted local image paths or trusted URLs only, and avoid passing untrusted remote image sources.

Risk: The output parameter allows writing to caller-supplied file paths.

Mitigation: Write outputs to a controlled workspace directory and avoid paths that could overwrite important files.

Risk: The setup script downloads npm dependencies and font assets during installation.

Mitigation: Pin and verify dependencies and downloaded fonts before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mewic/skills/content-news-thai)
- [Publisher profile](https://clawhub.ai/user/mewic)
- [Kanit Bold font source](https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Bold.ttf)
- [Kanit Light font source](https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Light.ttf)
- [Sarabun SemiBold font source](https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-SemiBold.ttf)
- [Prompt Bold font source](https://github.com/google/fonts/raw/main/ofl/prompt/Prompt-Bold.ttf)

## Skill Output:

**Output Type(s):** [Files, Text, JSON, Shell commands, Guidance]

**Output Format:** [JPEG image file plus JSON status output and caption guidance in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates 1080x1350 JPEG social images; accepts JSON parameters for headline, sub-headline, badge, colors, background image, attribution, brand name, and output path.]

## Skill Version(s):

1.0.0 (source: release evidence, scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
