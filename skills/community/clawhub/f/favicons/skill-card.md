## Description:

Use the favicons Node.js library to generate multi-platform website icons (Favicons).

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and website maintainers use this skill to generate favicon, app icon, PWA manifest, browser configuration, and HTML tag outputs from a source logo image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator writes many image, manifest, browser configuration, and HTML tag files into the chosen output directory.

Mitigation: Run it against a dedicated output directory and review generated files before merging them into an existing site.

Risk: The skill depends on the external favicons Node.js package.

Mitigation: Pin favicons to a reviewed exact version and use a lockfile in projects where dependency integrity matters.

Risk: Invalid source images or malformed JSON configuration can cause generation failure.

Mitigation: Use a clear PNG or SVG source image, validate JSON configuration before execution, and confirm Node.js and favicons are installed.

## Reference(s):

- [Favicons Configuration Reference](references/config_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/favicons)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; generated assets include PNG/ICO files, manifest.json, browserconfig.xml, and favicon-tags.html.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 14, an installed favicons package, a source image, an output directory, and optional JSON configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
