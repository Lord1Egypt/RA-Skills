## Description: <br>
Use when the user needs to integrate OpenClaw with Alibaba Cloud SLS/Observability, including collector setup, machine groups, indexes, dashboards, collection configs, or Logtail bindings on Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to provision Alibaba Cloud SLS observability for OpenClaw on Linux hosts, including collector setup, logstore indexing, dashboards, collection configuration, and machine-group binding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can persistently upload broad OpenClaw session logs from local users to Alibaba Cloud SLS. <br>
Mitigation: Install only when that data flow is intended, narrow collector FilePaths to the intended user or project, and review collected paths before enabling the collector. <br>
Risk: The setup uses sudo and Alibaba Cloud credentials while installing and configuring collector services. <br>
Mitigation: Use least-privilege temporary credentials, confirm required environment variables, validate ALIYUN_UID, and review the downloaded LoongCollector installer path before execution. <br>
Risk: Collector identifiers and services may remain on the host after the integration is no longer needed. <br>
Mitigation: Plan how to stop the collector service and remove /etc/ilogtail identifiers when disabling the integration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-sls-openclaw-integration) <br>
- [Command flow](references/cli-commands.md) <br>
- [Index definition](references/index.json) <br>
- [Audit dashboard template](references/dashboard-audit.json) <br>
- [Gateway dashboard template](references/dashboard-gateway.json) <br>
- [Collector config template](references/collector-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux host access, sudo, aliyun CLI access, Alibaba Cloud credentials, PROJECT, LOGSTORE, and ALIYUN_UID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
