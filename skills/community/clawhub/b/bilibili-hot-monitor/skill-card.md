## Description: <br>
生成 B站热门视频日报，使用字幕和可选 LLM 总结内容，并可通过邮件发送报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jacobzwj](https://clawhub.ai/user/Jacobzwj) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External users and developers use this skill to collect popular Bilibili videos, generate a structured daily Markdown report with optional AI summaries and commentary, and send the report by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a live Bilibili session cookie, an OpenRouter API key, and SMTP credentials, and may store them in a local plaintext config file. <br>
Mitigation: Prefer environment variables or dedicated low-risk accounts, avoid command-line secrets, restrict access to bilibili-monitor.json, and delete the file after use when possible. <br>
Risk: The skill can send generated report content to configured email recipients. <br>
Mitigation: Confirm the recipient list and report content before sending email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jacobzwj/bilibili-hot-monitor) <br>
- [Bilibili API WBI signature reference](https://socialsisteryi.github.io/bilibili-API-collect/docs/misc/sign/wbi.html) <br>
- [Bilibili video summary API reference](https://socialsisteryi.github.io/bilibili-API-collect/docs/video/summary.html) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [Google app passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report, optional HTML email, and inline shell commands or configuration prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3; report length depends on the configured number of videos and whether AI summaries are enabled.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
