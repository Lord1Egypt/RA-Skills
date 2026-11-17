## Description:

This Spanish-language skill helps an agent clone and improve the visual style of an Instagram or TikTok carousel from a screenshot or link, write new carousel copy for the user's topic and brand, and render final PNG slides from HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content teams use this skill to turn a reference carousel screenshot or social-media link into an original carousel in a similar visual style, with improved hook, readability, narrative flow, and CTA. The workflow is intended for creating new brand-owned content, not copying third-party post content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram or TikTok links may be processed through Apify or other scraping services.

Mitigation: Ask for user approval before external fetching, avoid private or sensitive posts, and accept user-provided screenshots as the fallback input.

Risk: Downloaded reference media and optional user photos may be stored in session or output folders.

Mitigation: Use only necessary images, keep them in the intended workspace folders, and avoid private or sensitive media unless the user explicitly provides it for this task.

Risk: Cloning a third-party visual style can raise copyright or platform-term concerns if the source content is copied too closely.

Mitigation: Use the reference to extract a design system only, write new user-owned content, and review copyright and platform-term implications before publishing.

Risk: Rendering loads Google Fonts and relies on a local Chrome or Chromium installation.

Mitigation: Confirm remote font loading is acceptable for the workspace and provide the HTML output if Chrome or Chromium is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/clonador-carrusel-formula100k)
- [capa-mejora-f100k.md](references/capa-mejora-f100k.md)
- [descargar-referencia.md](references/descargar-referencia.md)
- [extraccion-adn.md](references/extraccion-adn.md)
- [plantilla-html.md](references/plantilla-html.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Spanish Markdown guidance with HTML/CSS/JavaScript snippets, shell commands, and PNG slide files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically produces 4:5 carousel slides at 1080x1350px, rendered as ordered PNG files from a single HTML carousel.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact metadata reports 1.1.0 and package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
