## Description: <br>
Detect flood events by comparing water levels to thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and water-data analysts use this skill to guide an agent in detecting flood days from water-level time series, classifying severity when thresholds are available, and producing flood-event reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect flood thresholds or mismatched water-level units can produce misleading flood detection results. <br>
Mitigation: Confirm flood thresholds and units for each station before using the analysis output. <br>
Risk: Generated CSV or JSON reports may be written to local paths that expose sensitive operational data. <br>
Mitigation: Choose output locations deliberately and apply local data-handling controls before sharing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/flood-risk-analysis-flood-detection) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and CSV or JSON report patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create local CSV or JSON flood reports from water-level data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
