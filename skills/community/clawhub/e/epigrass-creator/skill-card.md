## Description: <br>
Create Epigrass epidemiological metapopulation models through guided specification for SIR, SEIR, SEIS, SIS, SI, or custom models, including geographic networks and GeoPackage import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fccoelho](https://clawhub.ai/user/fccoelho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, public health analysts, and researchers use the skill to specify Epigrass compartmental metapopulation models, import or enter geographic sites, configure parameters and connections, and generate runnable model files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wizard reads geospatial files from paths supplied by the user. <br>
Mitigation: Use only intended local GeoPackage, Shapefile, or GeoJSON inputs and avoid pointing the wizard at sensitive files. <br>
Risk: Generated model files are written into a local output directory and may replace existing files with the same names. <br>
Mitigation: Use a fresh output folder for each generated model and review the target path before writing files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fccoelho/epigrass-creator) <br>
- [Epigrass Project Homepage](https://github.com/fccoelho/epigrass) <br>
- [Epigrass Documentation](https://epigrass.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Interactive prompts and generated files, including model.epg, sites.csv, edges.csv, and model_spec.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads geospatial files only when the user provides a path and writes model outputs to a local output directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
