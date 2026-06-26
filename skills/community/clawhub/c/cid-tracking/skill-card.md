## Description: <br>
Generates CID tracking links, posts conversion events, fetches ad data, analyzes ROI, detects campaign anomalies, and produces Excel reports for OceanEngine, Kuaishou, and Tencent advertising workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaohang497-tech](https://clawhub.ai/user/zhaohang497-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advertising operations teams use this skill to create platform-specific CID links, collect campaign data, post conversion events, analyze ROI, detect anomalies, and generate Excel reports for domestic e-commerce ad campaigns. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Ad platform credentials and access tokens may be exposed if config.json is committed or shared. <br>
Mitigation: Keep config.json out of source control, rotate credentials, and grant only the minimum platform permissions needed. <br>
Risk: Tracking URLs or conversion payloads may include persistent identifiers or sensitive order fields. <br>
Mitigation: Avoid putting IMEI or other persistent identifiers in URLs and review each conversion or order field before sending it to an ad platform. <br>
Risk: Automated cron jobs and alert forwarding may distribute campaign or conversion data beyond the intended audience. <br>
Mitigation: Approve scheduled jobs and WeChat/DingTalk-style alert forwarding before enabling them, and restrict notification recipients. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaohang497-tech/cid-tracking) <br>
- [OceanEngine API reference](references/oceanengine_api.md) <br>
- [Kuaishou API reference](references/kuaishou_api.md) <br>
- [Tencent API reference](references/tencent_api.md) <br>
- [CID tracking best practices](references/cid_best_practices.md) <br>
- [OceanEngine open platform](https://oceanengine.github.io/open-platform/) <br>
- [Tencent advertising developer platform](https://e.qq.com/dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Excel reports, Text alerts, Tracking URLs] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts generate JSON files, tracking URLs, alert text, and .xlsx reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python dependencies and user-supplied ad platform credentials; generated files depend on selected script options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
