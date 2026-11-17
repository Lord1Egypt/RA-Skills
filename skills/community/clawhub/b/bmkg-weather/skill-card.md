## Description:

Gets Indonesian weather forecasts, early weather warnings, and earthquake data from BMKG public data sources without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thommyid](https://clawhub.ai/user/thommyid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Indonesia-specific weather, rainfall, temperature, wind, humidity, early warning, and earthquake questions with BMKG attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts BMKG public endpoints with the relevant region code or requested location context.

Mitigation: Use it for Indonesia weather and earthquake requests where sending location context to BMKG public services is acceptable.

Risk: Ambiguous Indonesian weather phrases may activate the skill even when the user has not named a precise location.

Mitigation: Ask for clarification when the location is unclear instead of guessing a specific region code.

Risk: BMKG data availability, API responsiveness, and update cadence can affect answer freshness.

Mitigation: Tell users when BMKG data cannot be retrieved and direct them to the BMKG public weather site for manual checking.

## Reference(s):

- [BMKG Weather Forecast API](https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah})
- [BMKG Early Weather Warning](https://data.bmkg.go.id/peringatan-dini-cuaca/)
- [BMKG Latest Earthquake Data](https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json)
- [BMKG Recent Earthquake Data](https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json)
- [BMKG Public Weather Site](https://cuaca.bmkg.go.id)
- [Kode Wilayah Reference](references/kode-wilayah.md)
- [Wilayah SQL Reference](references/wilayah.sql)
- [ClawHub Skill Page](https://clawhub.ai/thommyid/skills/bmkg-weather)
- [ClawHub Publisher Profile](https://clawhub.ai/user/thommyid)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with optional shell commands and summarized weather or earthquake data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should cite BMKG as the data source and may include localized weather fields such as temperature, humidity, wind, cloud cover, visibility, rainfall, and earthquake details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
