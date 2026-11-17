## Description:

Content Card helps an agent turn text, URLs, or files into shareable PNG visual cards in long-form, infographic, or multi-card layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to convert articles, notes, analysis, or structured information into polished PNG cards for reading, infographics, or social sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied web, file, or pasted content may be rendered through executable HTML and Chromium paths.

Mitigation: Use the skill only with trusted content, review generated HTML before capture, and sanitize or strip active content before browser rendering.

Risk: Browser rendering with networking enabled can fetch external resources during card generation.

Mitigation: Run capture in a restricted environment, block outbound network access where possible, and avoid sensitive projects until network controls are documented.

Risk: Local HTML and PNG generation can expose sensitive source material if credentials or private content are included.

Mitigation: Remove API keys, tokens, passwords, and private data from inputs and generated structured-content files before rendering.

Risk: Runtime behavior depends on Node, Playwright, Chromium, and template files.

Mitigation: Install from the checked-in lockfile, verify dependency versions, and scan templates and scripts before deployment.

## Reference(s):

- [ClawHub Content Card Release](https://clawhub.ai/lovensky1992-wk/skills/content-card)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Long Reading Card Mode](references/mode-long.md)
- [Infographic Mode](references/mode-infograph.md)
- [Poster Card Mode](references/mode-poster.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Taste Guidelines](references/taste.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [PNG image files with generated HTML and Markdown intermediates when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default canvas width is 1080 pixels; long-form and infographic modes may use full-page screenshots.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
