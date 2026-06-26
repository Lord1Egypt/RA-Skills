## Description: <br>
Download water level data from USGS using the dataretrieval package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve real-time or historical USGS stream gage data, including gage height, discharge measurements, site metadata, and station-based downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to install and use the dataretrieval Python package. <br>
Mitigation: Install it in a virtual environment and pin or review the dataretrieval package version before use. <br>
Risk: Large station lists or long date ranges can trigger many outbound requests to USGS, rate limits, or large downloads. <br>
Mitigation: Break large requests into smaller date ranges or station batches, add retry handling, and expect USGS availability or rate-limit responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/flood-risk-analysis-usgs-data-download) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example station IDs, USGS parameter codes, NWIS function guidance, and common download troubleshooting notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
