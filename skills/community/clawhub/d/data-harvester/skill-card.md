## Description: <br>
智能数据采集器 automates collection, cleaning, scheduling, and export of data from web pages, APIs, databases, and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxg852621787](https://clawhub.ai/user/dxg852621787) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure repeatable data collection jobs, process collected records, and export results as structured files or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive credentials to collect data from APIs, databases, and other configured systems. <br>
Mitigation: Use least-privilege, read-only credentials, avoid sharing admin or publishing tokens, and review each configured source before running collection. <br>
Risk: Security evidence reports under-disclosed OpenClaw platform-management methods that could install, uninstall, execute, or upload other skills if given a valid API key. <br>
Mitigation: Do not provide OpenClaw admin or publishing tokens unless those actions are explicitly intended and reviewed. <br>
Risk: Scheduled collection can repeatedly access external systems and export data to local paths. <br>
Mitigation: Enable scheduled jobs only after reviewing the target systems and write exports only to approved, non-sensitive locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxg852621787/data-harvester) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [OpenClaw homepage](https://openclawx.asia) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, configuration objects, and exported data files such as JSON, CSV, Excel, SQLite, or PDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can schedule repeated collection jobs and write exported datasets or reports to configured paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
