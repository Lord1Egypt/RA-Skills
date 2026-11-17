## Description:

Builds monthly visual activity calendars for Skool communities from weekly routines, dated events, and brand themes, then renders them with local HTML and Chrome into publishable assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External community operators and agents use this skill to turn a Skool community's recurring sessions, one-off events, and visual theme into a monthly activity calendar. It supports creating a calendar from scratch or cloning and adjusting the prior month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs npm dependencies and relies on a Puppeteer dependency tree.

Mitigation: Review, update, or pin dependencies before production or multi-user use.

Risk: Calendar configuration and brand assets are stored and read locally.

Mitigation: Use trusted local calendar text, logos, and paths, and keep per-community configs in controlled workspace locations.

Risk: Generated HTML is rendered through a local Chrome or Chromium binary.

Mitigation: Render only trusted configs/assets and review the generated PNG and HTML before publishing or sending them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/calendario-actividades-skool-f100k)
- [Catálogo de Dinámicas y Eventos · Metodología F100K](artifact/referencias/dinamicas-y-eventos.md)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell commands; rendered PNG and editable HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local npm dependencies and a Chrome or Chromium executable for rendering.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
