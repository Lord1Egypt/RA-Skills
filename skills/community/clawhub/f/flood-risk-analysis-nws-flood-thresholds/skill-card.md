## Description: <br>
Download flood stage thresholds from NWS (National Weather Service) for determining flood levels for USGS stations, accessing action/minor/moderate/major flood stages, or matching stations to flood thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve and clean NWS flood threshold data, filter stations by state and USGS ID, and match flood thresholds to station observations. It supports flood-risk analysis workflows, but should not be the sole basis for operational flood-safety decisions. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches external public CSV data from NWS, and the downloaded schema may be malformed or change over time. <br>
Mitigation: Validate the CSV headers and row widths before loading the data; the artifact specifically truncates rows to match the header count. <br>
Risk: Missing thresholds or -9999 placeholder values can produce incorrect flood-threshold matches. <br>
Mitigation: Convert threshold columns to numeric values and filter out missing values and -9999 placeholders before comparing station observations. <br>
Risk: USGS station IDs can lose leading zeros if treated as numbers. <br>
Mitigation: Preserve USGS IDs as strings and match stations using normalized string values. <br>
Risk: Flood-threshold guidance can be mistaken for operational safety advice. <br>
Mitigation: Use the skill as analysis guidance only and consult authoritative NWS, local emergency management, and domain experts for operational flood-safety decisions. <br>


## Reference(s): <br>
- [NWS National Water Prediction Service all gauges CSV](https://water.noaa.gov/resources/downloads/reports/nwps_all_gauges_report.csv) <br>
- [NWS National Water Prediction Service gauge pages](https://water.noaa.gov/gauges/<station_id>) <br>
- [Example NWS gauge page](https://water.noaa.gov/gauges/04118105) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with inline Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers CSV download, schema cleanup, threshold filtering, and USGS station matching.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
