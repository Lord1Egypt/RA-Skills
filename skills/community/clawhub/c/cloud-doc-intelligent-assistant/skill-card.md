## Description: <br>
Fetches public cloud provider documentation, stores local copies, detects documentation changes, and returns raw content and diffs for the calling agent to summarize or compare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mrb-AIA](https://clawhub.ai/user/Mrb-AIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to collect Aliyun, Tencent Cloud, Baidu Cloud, and Volcano Engine documentation, build local baselines, check for changes, and provide source material for downstream summaries, comparisons, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public cloud documentation and stores local copies, which may create local data retention obligations. <br>
Mitigation: Review the configured SQLite, cache, log, and notification paths and apply normal retention or cleanup controls for the deployment environment. <br>
Risk: Monitoring summaries can be sent to configured webhook destinations. <br>
Mitigation: Keep webhook delivery disabled unless needed, use trusted HTTPS endpoints, and verify destination configuration before enabling notifications. <br>
Risk: Unpinned package ranges can resolve to newer dependency versions over time. <br>
Mitigation: Use a locked dependency file for production deployments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Mrb-AIA/cloud-doc-intelligent-assistant) <br>
- [Cloud API contracts](references/cloud-api-contracts.md) <br>
- [OpenClaw integration notes](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with structured machine fields, brief human-readable text or markdown, diffs, and operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local SQLite data, logs, cached content, and notification markdown files when configured.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
