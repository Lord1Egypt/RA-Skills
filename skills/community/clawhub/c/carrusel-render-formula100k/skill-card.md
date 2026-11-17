## Description:

Converts an existing Formula 100K carousel script into branded 1080x1350 Instagram PNG slides with optional real-photo layouts and Chromium/Puppeteer export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social-media operators use this skill to turn a finished carousel script into Formula 100K-branded visual PNG slides for Instagram. It focuses on rendering and export, not writing the carousel script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read selected personal photos while preparing carousel slides.

Mitigation: Use explicit photo paths, review the selected images before rendering, and avoid granting broad access to unrelated photo folders.

Risk: The renderer may install npm dependencies and run Node/Chromium to export PNG files.

Mitigation: Run dependency audits or updates before deployment and execute the export in the intended workspace with the expected Chromium binary.

Risk: Chromium export can contact external font hosts when network-loaded fonts are used.

Mitigation: Disable or allowlist network requests during export, or constrain rendering to approved font sources.

Risk: Rendered files may be written outside the expected carousel output location if paths are chosen carelessly.

Mitigation: Keep outputs in the intended entregables/carruseles folder and verify generated PNG paths before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/carrusel-render-formula100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [Brandkit visual](brandkit.md)
- [Composition patterns](references/composiciones.md)
- [Real photo patterns](references/fotos-reales.md)
- [Canonical carousel example](references/ejemplo-completo.html)
- [Editorial dark rendering reference](references/editorial-oscuro-motor.js)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with HTML/CSS/JavaScript snippets and PNG file outputs from the export script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ordered 1080x1350 carousel PNG slides at 2x scale when Chromium and puppeteer-core are available.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
