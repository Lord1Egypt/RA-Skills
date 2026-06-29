## Description: <br>
Find or verify parcel vertex coordinates on the Cote d'Ivoire Mining Cadastre Map Portal/Landfolio site when a user provides an official parcel or license code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeromeex](https://clawhub.ai/user/jeromeex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve current parcel boundary vertices from the Cote d'Ivoire cadastre portal, convert Web Mercator geometry to WGS84, and report decimal-degree and DMS coordinates with the evidence source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to control a browser, evaluate in-page JavaScript, and possibly inspect network responses on the cadastre portal. <br>
Mitigation: Use the workflow only for intended parcel or license lookups, keep outputs tied to visible portal details or extracted geometry, and avoid treating prior lookup results as stable. <br>
Risk: Visually reconstructed coordinates may be less reliable than official in-page Esri geometry. <br>
Mitigation: Prefer official in-page Esri geometry when available, label visual reconstruction clearly, and verify reconstructed coordinates against portal evidence before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeromeex/skills/ci-cadastre-vertices) <br>
- [Cote d'Ivoire Mining Cadastre Map Portal](https://portals.landfolio.com/CoteDIvoire/en/) <br>
- [Active Licences ArcGIS MapServer](https://mines.gouv.ci.cadastreminier.org/arcgis/rest/services/MapPortal/ActiveLicences/MapServer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports parcel code, visible portal details, coordinate source, coordinate system, coordinate format, and vertices; includes both DMS and decimal degrees unless the user asks for only one format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
