## Description:

Plan Argentina trips with region-specific routing, money strategy, seasonal timing, and practical travel logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to design practical Argentina itineraries that account for entry rules, money and payments, seasonal timing, regional routing, transport, parks, safety, and day-to-day execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Argentina trip notes may include sensitive personal details and persist locally in ~/argentina/memory.md.

Mitigation: Review stored trip notes before and after use, avoid saving unnecessary sensitive details, and delete the memory file when prior trip context should no longer be reused.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/argentina)
- [Skill Homepage](https://clawic.com/skills/argentina)
- [Argentina Skill Sources](artifact/sources.md)
- [Argentina Migraciones - Tourists](https://www.argentina.gob.ar/migraciones/turistas)
- [AFIP/ARCA Travelers - Cash Entry and Exit](https://www.afip.gob.ar/viajeros/ayuda/ingreso-egreso-de-valores.asp)
- [Argentina National Parks Tariffs](https://www.argentina.gob.ar/parquesnacionales/tarifas)
- [SMN Weather Alerts](https://www.smn.gob.ar/alertas)
- [U.S. State Department - Argentina Country Information](https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/Argentina.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown travel guidance with optional shell commands and local memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use ~/argentina/memory.md to persist trip context; does not require external tools or network access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
