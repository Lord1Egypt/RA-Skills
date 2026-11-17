## Description:

Creates weekly Spanish content calendars for reels or carousel posts using the Formula 100K method, with Markdown previews and CSV/XLSX calendar files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams and creators use this skill to turn ready scripts, loose ideas, or reference links into a Monday-Sunday production calendar for reels or carousel posts. It assigns content by campaign purpose, suggests matching formats and CTAs, and prepares deliverables for review and production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger paid third-party research or transcription services for viral reference discovery.

Mitigation: Require explicit user approval before network research or paid Apify/Supadata-style calls.

Risk: Excel output depends on openpyxl and the scanner notes unpinned environment package installation guidance.

Mitigation: Preinstall and pin openpyxl in the execution environment, or allow CSV-only output when XLSX support is unavailable.

Risk: Client profile or campaign details may be sent to configured research tools during reference discovery.

Mitigation: Avoid providing private client details unless the user accepts sending that context to the configured tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/calendarizador-contenido-formula100k)
- [slots-por-modo.md](artifact/references/slots-por-modo.md)
- [catalogo-40-formatos.md](artifact/references/catalogo-40-formatos.md)
- [ejemplos-cta.md](artifact/references/ejemplos-cta.md)
- [generate_calendar.py](artifact/references/generate_calendar.py)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, guidance]

**Output Format:** [Markdown preview plus CSV and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reels calendars can produce CSV and XLSX; carousel calendars produce XLSX only. XLSX output depends on openpyxl availability.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
