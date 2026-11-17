## Description:

Routes carousel requests to Formula 100K formats, helps draft slide-by-slide scripts, anchors the visual reference, and returns platform-ready prompts or HTML for rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to choose Formula 100K carousel formats, draft Spanish slide scripts, prepare Gemini or ChatGPT prompts, and optionally generate HTML or PNG slide files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate and render local carousel HTML through Chrome.

Mitigation: Use only trusted specs and HTML, and review rendered PNGs before sharing or publishing them.

Risk: Specs may point the renderer at local image files and an output folder.

Mitigation: Provide only photos intended for the carousel and choose an output folder suitable for generated HTML and PNG files.

Risk: Optional image-generation or Telegram delivery workflows may incur cost or send content externally.

Mitigation: Confirm paid generation and delivery steps with the user before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/carrusel-formatos-f100k)
- [catalogo.md](artifact/references/catalogo.md)
- [prompts-por-plataforma.md](artifact/references/prompts-por-plataforma.md)
- [grimorio-carruseles.md](artifact/references/grimorio-carruseles.md)
- [estilos-guia-maestra.md](artifact/references/estilos-guia-maestra.md)
- [plantillas.md](artifact/references/plantillas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Spanish Markdown guidance with slide tables, platform prompts, HTML snippets, JSON specs, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write carousel HTML and PNG slide files when local Node.js, puppeteer-core, and Chrome or Chromium are available; otherwise returns platform prompts.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
