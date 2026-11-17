## Description:

Detects anomalies in time-series data from CSV, Excel, JSON, pasted data, or API sources using Amazon Chronos-2 forecasting plus Z-score, MAD, IQR, and moving-average checks, then generates interactive HTML and CSV reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to detect unusual points, contextual anomalies, collective anomalies, and level shifts in business, IT, IoT, financial, and monitoring time-series data. It helps run the detection scripts, tune thresholds, inspect generated reports, and summarize findings for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs unpinned Python packages and report dependencies.

Mitigation: Run it in an isolated virtual environment or container, and preinstall reviewed and pinned dependencies where possible.

Risk: The skill downloads an unpinned Chronos model/source during execution.

Mitigation: Pin and review the model source before use in shared, production, or sensitive environments.

Risk: Generated HTML reports from untrusted JSON data may carry content-handling risk.

Mitigation: Avoid opening reports generated from untrusted JSON files and review report inputs before rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/anomaly-detection)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON, CSV, HTML]

**Output Format:** [Markdown guidance with bash commands, plus generated anomaly_data.json, anomalies.csv, time_series_with_detection.csv, and an interactive HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install Python dependencies and download the Chronos-2 model at runtime; anomaly findings require human review before action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
