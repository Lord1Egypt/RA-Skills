## Description: <br>
Fetches A-share market data including fund flow, stock news, chip distribution, dragon-tiger list entries, limit-up stocks, market anomalies, sector anomalies, and individual stock details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glory904649854](https://clawhub.ai/user/Glory904649854) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve public A-share market datasets through OpenClaw-compatible Python functions or a command-line entry point. It is suited for data collection workflows that need current market snapshots, stock-specific details, and structured result objects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install metadata includes mismatched and unpinned dependencies. <br>
Mitigation: Review package metadata before installation and install in an isolated Python environment with pinned, vetted dependency versions. <br>
Risk: Live public finance data requests can fail or return incomplete data when network access or upstream APIs are unavailable. <br>
Mitigation: Handle unsuccessful result objects explicitly and validate returned market data before using it in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Glory904649854/clouddream-a-data) <br>
- [Eastmoney](https://www.eastmoney.com) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Tabular data, Shell commands, Code] <br>
**Output Format:** [OpenClaw-style JSON objects with success, data, and message fields; command-line and Python function outputs may contain tabular market records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live public finance data requests and retry logic; results depend on network availability and upstream API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, setup.py, __init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
