## Description: <br>
Collects AMap POI data for medical beauty and life beauty businesses by city, then exports raw JSON data and an Excel summary workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supperwk](https://clawhub.ai/user/supperwk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and operators can use this skill to collect city-level AMap POI listings for medical beauty and life beauty organizations and produce JSON plus spreadsheet outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release publishes and uses a real AMap API key by default. <br>
Mitigation: Review before installing and supply a controlled AMap key with --key or AMAP_KEY instead of relying on the bundled key. <br>
Risk: Generated POI data is written into the OpenClaw workspace. <br>
Mitigation: Review workspace data handling and retention before running the skill on sensitive or regulated workflows. <br>
Risk: Excel export depends on openpyxl in the execution environment. <br>
Mitigation: Install openpyxl only in a trusted environment, or run with --skip-excel when spreadsheet output is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supperwk/amap-poi-fetch) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/supperwk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, API Calls, Configuration] <br>
**Output Format:** [JSON files, Excel workbook, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an AMap API key supplied with --key or AMAP_KEY; Excel export requires openpyxl and can be skipped with --skip-excel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
