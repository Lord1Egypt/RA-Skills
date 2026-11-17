## Description:

Find or verify parcel vertex coordinates on the Cote d'Ivoire Mining Cadastre Map Portal/Landfolio site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeromeex](https://clawhub.ai/user/jeromeex)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and GIS analysts use this skill to retrieve current parcel boundary vertices for a Cote d'Ivoire mining cadastre parcel or license code. The workflow reports portal result details, geometry source, coordinate system, coordinate format, and vertices in decimal degrees and DMS when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portal-derived parcel status, geometry, and existence can change over time.

Mitigation: Re-query the live cadastre portal during each run and report the visible portal result details and geometry source with the coordinates.

Risk: Visual reconstruction may be less reliable than official in-page Esri geometry.

Mitigation: Prefer exact-code Esri geometry from the loaded portal page, use visual reconstruction only as a fallback, and clearly label visually reconstructed coordinates as non-survey evidence.

Risk: Coordinate lookup output may be mistaken for legal survey data.

Mitigation: State that results are portal-derived evidence and should be independently verified before legal, operational, or boundary-sensitive use.

## Reference(s):

- [CI Cadastre Vertices ClawHub Skill Page](https://clawhub.ai/jeromeex/skills/ci-cadastre-vertices)
- [Cote d'Ivoire Mining Cadastre Map Portal](https://portals.landfolio.com/CoteDIvoire/en/)
- [Active Licences ArcGIS MapServer](https://mines.gouv.ci.cadastreminier.org/arcgis/rest/services/MapPortal/ActiveLicences/MapServer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown with portal evidence, coordinate tables, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports coordinate source and avoids treating visually reconstructed coordinates as surveyed boundary data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
