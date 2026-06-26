## Description: <br>
Generates and pushes daily news briefings for a configured domain, using recent search results and sending structured Markdown summaries through WeCom, Feishu, or webhook channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoyee94](https://clawhub.ai/user/shoyee94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure automated daily news reports for a chosen topic and send them to workplace chat or webhook destinations. It is suited for recurring domain monitoring where generated summaries and outbound delivery are acceptable after local configuration review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interactive setup can place raw user-provided values into an executable Python config file. <br>
Mitigation: Review generated config.py before execution, especially webhook headers, URLs, receiver IDs, and cron values. <br>
Risk: The workflow can send full generated reports to external chat or webhook destinations. <br>
Mitigation: Use only trusted destinations and verify that report contents are appropriate for the target channel before unattended use. <br>
Risk: OAuth, Authorization, receiver IDs, and webhook values may be sensitive. <br>
Mitigation: Store credentials securely, avoid sharing config.py, and rotate tokens if they are exposed. <br>
Risk: Cron scheduling enables repeated unattended outbound sends. <br>
Mitigation: Enable cron only for intended recurring delivery and monitor initial runs for correctness. <br>


## Reference(s): <br>
- [Configuration Guide](references/config.md) <br>
- [Daily Briefing Format](references/format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shoyee94/daily-news-push) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, Python configuration files, JSON-like channel payloads, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send full generated reports to configured WeCom, Feishu, or webhook destinations and can be scheduled with cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
