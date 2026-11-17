## Description:

Creates algorithmic art philosophies and p5.js interactive generative-art artifacts with seeded randomness and parameter controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and creators use this skill to turn a prompt into a computational art philosophy and a browser-ready p5.js artwork with seed navigation, tunable parameters, and download controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may contact cdnjs and Google Fonts when opened.

Mitigation: Review generated HTML before sharing or deploying, and bundle p5.js and fonts locally or add subresource integrity where appropriate.

Risk: Shared artifacts may appear Anthropic-styled because the template requires Anthropic branding.

Mitigation: Remove or neutralize Anthropic branding before general release unless that presentation is intentional and permitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pupuking723/skills/algorithmic-art-anthropic)
- [p5.js 1.7.0 CDN](https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js)
- [Google Fonts API](https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Lora:wght@400;500&display=swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown philosophy plus single-file HTML and p5.js code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses seeded randomness for reproducible variations; generated HTML may load p5.js from cdnjs and fonts from Google Fonts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
