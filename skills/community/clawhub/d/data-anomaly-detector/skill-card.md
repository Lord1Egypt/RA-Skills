## Description: <br>
Detect anomalies and outliers in construction data: unusual costs, schedule variances, productivity spikes. Statistical and ML-based detection methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction analysts, estimators, schedulers, and project teams use this skill to inspect user-provided cost, schedule, productivity, and sequence data for outliers, impossible values, duplicate records, and trend deviations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests filesystem access for construction or business datasets and optional report exports. <br>
Mitigation: Grant access only for specific datasets you intend to analyze and confirm export paths before allowing files to be written. <br>
Risk: Anomaly findings can be incomplete or misleading if source data, thresholds, grouping fields, or configuration are wrong. <br>
Mitigation: Review generated findings and suggested actions before relying on them for project, cost, schedule, or commercial decisions. <br>


## Reference(s): <br>
- [Data Driven Construction homepage](https://datadrivenconstruction.io) <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/data-anomaly-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown summaries, anomaly tables, Python code patterns, and export-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity counts, anomaly IDs, affected fields, expected ranges, confidence values, and suggested follow-up actions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
