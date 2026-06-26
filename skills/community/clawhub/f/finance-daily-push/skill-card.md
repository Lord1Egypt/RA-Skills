## Description: <br>
自动推送 A 股科技板块金融日报，含实时行情、重要消息解读和独立个股推荐，覆盖早报、晚报与周报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kldsw](https://clawhub.ai/user/kldsw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and operators use this skill to generate scheduled or ad hoc A-share technology-sector morning reports, evening reports, and weekly outlooks. It combines market data prompts, cron examples, and helper scripts for Tencent Finance and TuShare data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships and automatically uses a bundled TuShare API token when TUSHARE_TOKEN is not set. <br>
Mitigation: Review or remove the bundled token before installation, set your own TUSHARE_TOKEN, and rotate the exposed token if you own it. <br>
Risk: The skill can create automated finance-report schedules and call external data services. <br>
Mitigation: Install dependencies from trusted sources and create only the cron schedules and data-service calls that match the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kldsw/finance-daily-push) <br>
- [Publisher profile](https://clawhub.ai/user/kldsw) <br>
- [TuShare token setup](https://tushare.pro/user/token) <br>
- [TuShare registration](https://tushare.pro/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report templates with inline shell commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include source and timestamp annotations, A-share technology-sector analysis, stock recommendations, risk levels, and an investment disclaimer.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
