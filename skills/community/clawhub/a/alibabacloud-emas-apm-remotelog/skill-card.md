## Description: <br>
EMAS APM Remote Log (TLog) CLI Skill for remote log retrieval, task management, and log query operations via Alibaba Cloud CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to retrieve, manage, and query Alibaba Cloud EMAS APM remote logs for mobile applications through the Alibaba Cloud CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive mobile application logs from Alibaba Cloud EMAS. <br>
Mitigation: Use it only for EMAS apps you administer and limit queries by authorized device, time window, and keyword. <br>
Risk: Broad or long-lived Alibaba Cloud credentials could expose more access than the workflow needs. <br>
Mitigation: Use least-privilege RAM permissions, prefer short-lived credentials where possible, and never enter access keys in chat or shell history. <br>
Risk: Installer commands may download and execute code from Alibaba Cloud's CLI CDN. <br>
Mitigation: Inspect installer scripts or binaries before execution in sensitive environments and verify downloads come from the documented HTTPS host. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-emas-apm-remotelog) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies for EMAS APM Remote Log Operations](references/ram-policies.md) <br>
- [Related CLI Commands for EMAS APM TLog Operations](references/related-commands.md) <br>
- [Verification Method for EMAS APM TLog Operations](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/) <br>
- [CLI Credential Configuration](https://help.aliyun.com/zh/cli/configure-credentials) <br>
- [EMAS Mobile Monitoring Product](https://api.aliyun.com/product/emas-appmonitor) <br>
- [CreateTlogTask API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/CreateTlogTask) <br>
- [GetTlogDeviceList API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/GetTlogDeviceList) <br>
- [GetTlogDeviceInfo API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/GetTlogDeviceInfo) <br>
- [GetTlogCollectList API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/GetTlogCollectList) <br>
- [SearchTlog API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/SearchTlog) <br>
- [GetTlogTaskCollections API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/GetTlogTaskCollections) <br>
- [GetTlogTaskInfo API](https://api.aliyun.com/api/emas-appmonitor/2019-06-11/GetTlogTaskInfo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Alibaba Cloud CLI commands, parameter checks, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the Alibaba Cloud CLI emas-appmonitor plugin and require user-confirmed app, device, task, and time-window parameters.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
