## Description: <br>
Check AIClient2API usage statistics, quotas, account status, subscription status, and API consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limingdev-tech-2024](https://clawhub.ai/user/limingdev-tech-2024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect AIClient2API credits, quotas, free trial status, subscription details, and overage information from a local AIClient2API installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read ~/web/AIClient-2-API/configs/pwd and authenticate to a localhost AIClient2API service. <br>
Mitigation: Review the shell scripts before execution and run them only in an environment where access to that local password file and service is intended. <br>
Risk: The scripts can print account and billing-related usage details from usage-cache.json. <br>
Mitigation: Avoid sharing generated reports publicly and redact email, user ID, quota, subscription, and charge details before copying output. <br>
Risk: Refresh behavior depends on the local AIClient2API service and may update usage data before display. <br>
Mitigation: Use the documented cache-only path or inspect usage-cache.json directly when a read-only summary is sufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/limingdev-tech-2024/aiclient2api-usage) <br>
- [AIClient2API local web UI](http://127.0.0.1:16825) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and terminal output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account and billing-related usage details read from the local AIClient2API usage cache or localhost service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
