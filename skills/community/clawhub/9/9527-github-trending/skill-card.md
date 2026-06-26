## Description: <br>
Automatically fetches GitHub Trending repositories and sends daily notifications with language, time-window, and Telegram, DingTalk, or WeCom options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[863king](https://clawhub.ai/user/863king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to monitor GitHub Trending projects, filter results by language or time window, and deliver the resulting digest to chat channels or local output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository-interest digests may be sent to external chat providers. <br>
Mitigation: Use least-privilege bot credentials and avoid sending sensitive private project names or internal research interests through configured notifications. <br>
Risk: Cron scheduling can continue sending notifications after initial setup. <br>
Mitigation: Test the command manually before enabling the schedule and document the crontab entry or disable path for operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/863king/9527-github-trending) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON output, with shell command examples and notification configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports daily, weekly, and monthly time windows; optional language filtering; optional Telegram, DingTalk, and WeCom delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
