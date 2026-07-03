## Description: <br>
Detects anomalies in time-series data using Amazon Chronos-2 forecasts plus Z-Score, MAD, IQR, and moving-average checks, then exports JSON/CSV results and an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operations teams use this skill to analyze time-series metrics from files, pasted data, or API-derived datasets and identify point, contextual, collective, and level-shift anomalies for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages and download model artifacts during normal use. <br>
Mitigation: Run it in an isolated virtual environment or container, and review or pin dependencies before execution. <br>
Risk: Datasets and generated reports may contain sensitive operational or business data. <br>
Mitigation: Avoid sensitive datasets unless temporary file locations, output directories, and report handling are approved. <br>
Risk: Anomaly labels and severity levels can be misleading without domain context. <br>
Mitigation: Treat outputs as analysis aids and require human review before operational or business action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/anomaly-detection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON and CSV result files, and an interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces anomaly_data.json, anomalies.csv when anomalies exist, time_series_with_detection.csv, and a Plotly-based HTML report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
