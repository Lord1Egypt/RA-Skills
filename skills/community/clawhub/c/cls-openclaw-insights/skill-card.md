## Description: <br>
Analyzes OpenClaw monitoring logs and metrics stored in Tencent Cloud Log Service to help investigate cost, performance, runtime exception, and audit questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trumphuang](https://clawhub.ai/user/trumphuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw CLS log and metric topics, build CQL, SQL, and PromQL queries, and troubleshoot token cost, latency, queues, gateway errors, webhooks, instances, and agent activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tencent Cloud credentials to read OpenClaw CLS logs and metrics, which may include operational, session, audit, or token usage data. <br>
Mitigation: Use least-privilege temporary credentials, confirm the selected region and topic, and limit queries to the minimum time range and fields needed. <br>
Risk: Raw log and audit results may contain sensitive operational details. <br>
Mitigation: Review outputs before sharing them and avoid exposing unnecessary session, audit, or runtime log content. <br>
Risk: The skill installs Python dependencies used to call Tencent Cloud and Prometheus-compatible APIs. <br>
Mitigation: Install with current patched or locked dependency versions and review dependency updates before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/trumphuang/cls-openclaw-insights) <br>
- [Tencent Cloud CLS API Reference for OpenClaw](references/cls_api_reference.md) <br>
- [Tencent Cloud CLS Application Center](https://console.cloud.tencent.com/cls/cloud-product) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, query examples, JSON API responses, and analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include CQL, SQL, PromQL, Tencent Cloud CLS API calls, credential setup guidance, and monitoring analysis summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
