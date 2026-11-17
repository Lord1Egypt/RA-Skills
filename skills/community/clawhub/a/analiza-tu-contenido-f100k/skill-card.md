## Description:

Hace el modulo Analiza tu Contenido de Formula 100K sobre la cuenta de Instagram de la alumna y entrega una Hoja del Mes en HTML con lectura de filtros, conclusiones fijas y calendario de contenido.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and content operators use this skill to analyze an owner-controlled Instagram account, combine Reels metrics and transcripts, identify blocked content filters, and produce a monthly action plan. The agent outputs structured data, conclusions, and an HTML report that guides next-month content decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow could be used to analyze Instagram accounts that the requester does not control or have consent to analyze.

Mitigation: Use it only for accounts controlled by the requester or covered by explicit consent, and prefer the Composio connected-account path over unofficial scraping fallbacks.

Risk: Generated datos.json and HTML reports may contain private business metrics, content strategy, and account performance details.

Mitigation: Store monthly working folders and reports in restricted locations, share reports only with intended recipients, and remove stale artifacts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/analiza-tu-contenido-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [Advanced screenshot requirements](artifact/references/capturas.md)
- [Input and output schemas](artifact/references/esquema.md)
- [Format library](artifact/references/formatos.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Spanish Markdown guidance with JSON schemas, Node.js shell commands, structured JSON outputs, and a generated single-file HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses datos.json as the main input, can emit resultado.json for engine analysis, and can render hoja-del-mes.html from datos.json plus lectura.json.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
