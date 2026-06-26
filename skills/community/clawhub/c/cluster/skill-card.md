## Description: <br>
Cluster performs data clustering analysis with k-means and hierarchical algorithms for grouping, classifying, or segmenting numerical datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to run local clustering on numeric CSV or JSONL datasets, evaluate cluster quality, assign new points, and export or visualize results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clustering history stored in ~/.cluster may retain source file paths, assignments, centroids, and metrics that reveal sensitive dataset details. <br>
Mitigation: Avoid highly sensitive datasets unless local retention is acceptable, and delete ~/.cluster data when it is no longer needed. <br>
Risk: The skill runs a local bash/Python script that reads input files and can write exports or configuration files. <br>
Mitigation: Review the script before use and provide only intended local input, output, and configuration paths. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Cluster on ClawHub](https://clawhub.ai/ckchzh/cluster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Terminal text with optional JSON, CSV, or JSONL exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local numeric CSV or JSONL inputs and stores clustering history in ~/.cluster/data.jsonl with configuration in ~/.cluster/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
