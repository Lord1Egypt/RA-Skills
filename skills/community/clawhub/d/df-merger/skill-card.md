## Description: <br>
Merge pandas DataFrames from multiple construction sources. Handle different schemas, keys, and data quality issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction data practitioners and developers use this skill to merge BIM, schedule, cost, quantity, sensor, and other project DataFrames while reconciling schema differences and inconsistent keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local file access and may export merged results. <br>
Mitigation: Limit filesystem access to the specific input files needed for a merge and review any export path before writing CSV, Excel, or JSON outputs. <br>
Risk: Broad construction-task activation may exceed the skill's useful data-merging scope. <br>
Mitigation: Use it for DataFrame merging tasks and route unrelated construction management requests to a more appropriate skill. <br>
Risk: Fuzzy key matching and schema harmonization can produce incorrect joins when columns or values are ambiguous. <br>
Mitigation: Review merge keys, match scores, row counts, and summary statistics before relying on merged data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/df-merger) <br>
- [DataDrivenConstruction homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown with structured tables, summary statistics, and Python code blocks when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May offer CSV, Excel, or JSON exports when relevant.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release metadata; claw.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
