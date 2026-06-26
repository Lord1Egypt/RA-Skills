## Description: <br>
Alibaba Cloud WAF Bot Management automated configuration assistant that helps evaluate, configure, verify, and tune bot protection policies through OpenAPI and Alibaba Cloud CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to assess Alibaba Cloud WAF Bot Management readiness, recommend scenario-specific bot protection rules, apply CLI/OpenAPI configuration changes, and review effectiveness for LLM APIs, retail promotions, general anti-crawling, and academic research platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real production Alibaba Cloud WAF security-policy changes. <br>
Mitigation: Use least-privilege RAM permissions, begin with read-only assessment or monitor/canary mode, and require explicit approval before create, modify, enable, delete, or clear-address operations. <br>
Risk: Misconfigured bot rules can block legitimate users or disrupt protected applications. <br>
Mitigation: Review hit data before enforcement, whitelist trusted IP ranges, and switch actions gradually from monitor to captcha or block after false-positive checks. <br>
Risk: The workflow requires sensitive Alibaba Cloud credentials or tokens. <br>
Mitigation: Use the Alibaba Cloud default credential chain or temporary credentials and do not hardcode AK/SK values in scripts or skill materials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-waf-bot-management) <br>
- [Alibaba Cloud CLI Integration Example](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/cli-integration-example-v3) <br>
- [Attack Level x Protection Strategy Matching Matrix](references/attack-level-matrix.md) <br>
- [BOT 2.0 Rule Labels Quick Reference](references/bot2-rules-reference.md) <br>
- [WAF Bot Management OpenAPI Quick Reference](references/openapi-reference.md) <br>
- [RAM Policies for WAF Bot Management](references/ram-policies.md) <br>
- [Rules Not Recommended for Enablement](references/rules-blacklist.md) <br>
- [Academic Research Scene Configuration Manual](references/scene-academic.md) <br>
- [General Anti-Crawl Scene Configuration Manual](references/scene-anti-crawl.md) <br>
- [LLM API Scene Configuration Manual](references/scene-llm-api.md) <br>
- [Retail Promotion Scene Configuration Manual](references/scene-retail-promotion.md) <br>
- [SDK Integration Guide](references/sdk-integration-guide.md) <br>
- [SLS Query Templates Library](references/sls-query-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Alibaba Cloud CLI commands, JSON snippets, and SQL query templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assessment reports, rule recommendations, configuration change logs, verification checks, and rollback or tuning guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
