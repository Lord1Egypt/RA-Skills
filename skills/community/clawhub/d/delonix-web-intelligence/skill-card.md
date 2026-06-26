## Description: <br>
德胧外网舆情采集工具 helps an agent collect hotel-industry web intelligence, summarize search results, generate daily monitoring reports, and prepare Feishu card updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hotel operations, brand, public-relations, and competitive-intelligence teams use this skill to monitor external web mentions, competitor activity, complaints, industry trends, and daily hotel-sector news. It produces concise reports and Feishu-ready summaries for internal review and follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad hotel-industry monitoring triggers and scheduled delivery can produce or send reports before a reviewer confirms scope, recipients, keywords, and timezone. <br>
Mitigation: Keep scheduled delivery disabled until explicitly needed, replace example chat IDs, and confirm recipients, schedule, timezone, and keywords before enabling automation. <br>
Risk: Optional third-party collection or messaging tools may require additional authorization and operational review. <br>
Mitigation: Independently vet optional AutoCLI and Lark or Feishu tooling before installation or authorization. <br>
Risk: Search summaries and generated reports may contain incomplete or misleading claims about competitors, complaints, or public incidents. <br>
Mitigation: Review generated summaries and source links before acting on or redistributing important findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/delonix-web-intelligence) <br>
- [AutoCLI referenced optional tool](https://github.com/nashsu/AutoCLI.git) <br>
- [AutoCLI v0.3.7 referenced release asset](https://github.com/nashsu/AutoCLI/releases/download/v0.3.7/autocli-x86_64-unknown-linux-musl.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown reports, Feishu card markup, shell command examples, cron configuration, and optional JSON search output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files and raw search JSON under a dated temporary output directory when the bundled daily-report script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
