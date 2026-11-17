## Description:

Analyzes Instagram and TikTok profiles to identify top-performing content, sales angles, follower-growth signals, comment-driven content gaps, and a two-week action plan using the Formula 100K methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and growth consultants use this skill to audit Instagram or TikTok profiles, compare recent content performance, find audience demand in comments, and turn the evidence into an actionable content plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill contains conflicting instructions about using logged-in browser sessions to collect private account metrics.

Mitigation: Use it only for audits where the user clearly asks to analyze social profiles, and do not use a logged-in browser session unless the skill is rewritten with explicit ownership, consent, and data-handling controls.

Risk: Deep audits can involve paid scraping or collection from third-party services.

Mitigation: Ask for user approval before paid scraping; prefer Composio for the user's own professional account, Apify or Supadata for public data, or user-provided screenshots.

Risk: Some private metrics, such as retention or insights for accounts the user does not own, may be unavailable.

Mitigation: Mark unavailable private metrics as unavailable and avoid estimating them from public signals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/analizador-perfiles-formula100k)
- [Analisis de comentarios](references/analisis-comentarios.md)
- [Auditoria profunda con Apify](references/auditoria-profunda-apify.md)
- [Lectura de metricas](references/lectura-metricas.md)
- [Estructura del reporte](references/reporte-estructura.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, evidence notes, and optional shell or tool commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommendations to request user approval before paid scraping and to mark unavailable private metrics rather than estimating them.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
