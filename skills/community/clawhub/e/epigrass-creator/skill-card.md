## Description:

Create Epigrass epidemiological metapopulation models through guided specification, including SIR-family model selection, geographic networks, and GeoPackage-backed spatial imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fccoelho](https://clawhub.ai/user/fccoelho)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, researchers, and public-health modelers use this skill to create Epigrass metapopulation model files through a guided wizard. It supports model selection, epidemiological parameters, geographic site definition, network generation, and geospatial imports for simulation setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated model parameters, network edges, or flow estimates may be inaccurate if user inputs or assumptions are wrong.

Mitigation: Review model.epg, sites.csv, edges.csv, and model_spec.json with appropriate domain expertise before running or relying on simulation results.

Risk: Untrusted GeoPackage, Shapefile, or GeoJSON inputs can influence generated model files.

Mitigation: Install and run the skill in an isolated environment, use trusted or validated geospatial inputs, prefer pinned dependency versions, and inspect generated files before running epirunner.

Risk: The wizard writes generated artifacts into a user-selected output directory.

Mitigation: Use a dedicated empty output directory for each run to avoid overwriting or mixing simulation artifacts.

## Reference(s):

- [Epigrass Project](https://github.com/fccoelho/epigrass)
- [Epigrass Documentation](https://epigrass.readthedocs.io/)
- [GeoPackage Import Example](examples/geopackage_example.md)
- [ClawHub Skill Page](https://clawhub.ai/fccoelho/skills/epigrass-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated Epigrass script, CSV files, and JSON model specification.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model.epg, sites.csv, edges.csv, and model_spec.json in a user-selected output directory.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
