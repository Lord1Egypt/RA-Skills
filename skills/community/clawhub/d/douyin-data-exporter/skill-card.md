## Description: <br>
Exports Douyin user homepage video data and optional Dou+/BOSS advertising order data through Python API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to export Douyin account video lists for analysis or reporting, with optional advertising order export when a separate Dou+/BOSS bearer token and customer ID are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exports sensitive Douyin account data and optional advertising order data using bearer tokens. <br>
Mitigation: Use short-lived, least-privilege tokens and avoid passing long-lived bearer tokens directly in shell command history. <br>
Risk: Exported files may contain sensitive account or advertising data. <br>
Mitigation: Check the workspace output location before running and store or share generated JSON, CSV, and Excel files only in approved locations. <br>
Risk: Account names are used in generated file names. <br>
Mitigation: Use simple account names without slashes or path characters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ahsbnb/douyin-data-exporter) <br>
- [TikHub registration](https://user.tikhub.io/register) <br>
- [TikHub API base](https://api.tikhub.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, text] <br>
**Output Format:** [JSON, CSV, Excel, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and a TikHub token; optional Dou+/BOSS bearer token and customer ID enable advertising order export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
