## Description:

Generate an interactive Germany map of Odoo contacts with clickable markers that open the corresponding record in Odoo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernhmueller](https://clawhub.ai/user/bernhmueller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Odoo operators use this skill to generate an HTML map of German Odoo contacts for location review and quick navigation back to contact records.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: Odoo contact addresses and generated contact details may be exposed to third-party map or geocoding services.

Mitigation: Use stored coordinates or an approved internal geocoder for sensitive contacts, and review whether the generated HTML can contain protected contact data before sharing it.

Risk: The skill needs credentials or an API key to read Odoo contact records.

Mitigation: Prefer a read-only Odoo API key, provide credentials through the environment, and avoid keeping a skill-local .env file in shared or backed-up workspaces.

Risk: The generated map loads external Leaflet assets and OpenStreetMap tiles.

Mitigation: Bundle approved assets or use integrity controls and approved tile services before use with sensitive contact datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bernhmueller/skills/contact-map-bm)
- [Publisher profile](https://clawhub.ai/user/bernhmueller)
- [Nominatim search endpoint](https://nominatim.openstreetmap.org/search)
- [Leaflet assets CDN](https://unpkg.com/leaflet@1.9.4/dist/leaflet.js)
- [OpenStreetMap tile service](https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance and shell commands that run a Python script which writes an interactive HTML map file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Odoo connection settings and may geocode addresses when stored coordinates are missing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
