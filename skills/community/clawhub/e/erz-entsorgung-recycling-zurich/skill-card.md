## Description:

Abfuhrkalender für Zürich via OpenERZ API. Nutze bei Fragen zu Kehricht, Karton, Papier, Grüngut, Sonderabfall oder Entsorgungsterminen im Raum Zürich.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbjoern](https://clawhub.ai/user/mbjoern)

### License/Terms of Use:


## Use Case:

Zurich residents, support staff, and agents use this skill to look up waste, cardboard, paper, organic, special-disposal, and related collection dates for a Zurich postal code or area.

### Deployment Geography for Use:

Switzerland (Zurich)

## Known Risks and Mitigations:

Risk: Queries may send the selected Zurich area or postal code, date range, and waste-type filters to the public OpenERZ API.

Mitigation: Confirm the default postal code 8003 and requested filters are appropriate before using or sharing API queries.

Risk: Collection results depend on the OpenERZ API response for the selected area and date range.

Mitigation: For high-impact decisions, verify unusual or time-sensitive disposal dates with the official Zurich disposal schedule or collection service.

## Reference(s):

- [OpenERZ Calendar API](https://openerz.metaodi.ch/api/calendar)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses region, area or postal code, waste-type, date-range, sort, and limit parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
