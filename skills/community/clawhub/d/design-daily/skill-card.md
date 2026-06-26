## Description: <br>
Daily design industry brief for UI/UX designers and PMs, covering AI and design, design engineering, product experience breakdowns, and design decision logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tkk0124](https://clawhub.ai/user/Tkk0124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Design practitioners and product teams use this skill to fetch recent design-industry items, summarize them into a concise Chinese daily brief, and save shareable local outputs for review or discussion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Serper and DeepSeek API keys and setup.py can write them to a local .env file. <br>
Mitigation: Use dedicated low-limit keys and keep the generated .env file private. <br>
Risk: Normal runs make external API calls and save local TXT, JSON, and log files. <br>
Mitigation: Run preview mode first to inspect behavior before saving outputs. <br>
Risk: The optional cron command can create recurring daily API calls and local log files. <br>
Mitigation: Add the cron schedule only when recurring execution is intended. <br>


## Reference(s): <br>
- [Design Daily ClawHub release](https://clawhub.ai/Tkk0124/design-daily) <br>
- [Serper Search API endpoint](https://google.serper.dev/search) <br>
- [DeepSeek Chat Completions API endpoint](https://api.deepseek.com/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Chinese plain-text brief and JSON data saved under logs/, with optional preview output to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SERPER_API_KEY and DEEPSEEK_API_KEY; preview mode prints without saving files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
