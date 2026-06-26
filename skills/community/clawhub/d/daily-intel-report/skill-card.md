## Description: <br>
Daily Intel Report collects AI industry news and Zhejiang public procurement notices, filters recent and keyword-matched items, and formats a Chinese daily digest for Feishu or email delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce Chinese daily intelligence reports that combine current AI news with keyword-matched Zhejiang public procurement notices. It is suited for scheduled daily delivery, manual news retrieval, and procurement lead screening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public web sources and can include untrusted or stale source material in a daily report. <br>
Mitigation: Treat fetched articles and procurement notices as untrusted input, verify important items against the original source, and keep the documented timestamp filtering and deduplication checks enabled. <br>
Risk: Cron delivery can send reports to unintended recipients if Feishu, SMTP, or schedule settings are misconfigured. <br>
Mitigation: Confirm the schedule, recipient list, Feishu target, and SMTP settings before enabling automated delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lgugeng/daily-intel-report) <br>
- [Data Sources](references/data-sources.md) <br>
- [AIBase News](https://www.aibase.com/news) <br>
- [IT Home AI Channel](https://www.ithome.com/tags/AI/) <br>
- [Zhejiang Government Procurement Search](http://www.ccgp-zhejiang.gov.cn/portal/searchHome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, API calls, Guidance] <br>
**Output Format:** [Chinese Markdown or plain text digest with optional Python script output and delivery configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run on a daily Asia/Shanghai schedule, can send through Feishu DM or optional email, and maintains deduplication state in memory/last-pushed.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
