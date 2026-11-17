## Description:

Repairs incomplete ArcGIS Pro deep learning training-data exports by detecting supported metadata and image formats, then generating the standard EMD, accumulated statistics, map, and stats files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongjiekun](https://clawhub.ai/user/gongjiekun)

### License/Terms of Use:

MIT-0

## Use Case:

GIS developers and ArcGIS Pro users use this skill when exported deep learning training data is missing ArcGIS-recognized support files or is not recognized by Pro. It guides an agent to inspect the dataset folder, run the bundled repair script, and generate files required by Train Deep Learning Model workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair script can overwrite generated ArcGIS support files and delete non-standard .emd or .json files in the selected dataset folder.

Mitigation: Back up the dataset or run on a copy first, and review any existing .emd or .json files before executing the cleanup step.

Risk: Generated metadata and statistics are derived from the dataset contents and may be unsuitable if the folder structure or labels are incomplete or mismatched.

Mitigation: Inspect the detected format, classes, statistics, and ArcGIS Pro validation output before using the repaired dataset for training.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gongjiekun/skills/arcgis-training-data-fix)
- [Publisher profile](https://clawhub.ai/user/gongjiekun)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and Python-generated JSON/text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates esri_model_definition.emd, esri_accumulated_stats.json, map.txt, and stats.txt in the selected training-data folder.]

## Skill Version(s):

5.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
