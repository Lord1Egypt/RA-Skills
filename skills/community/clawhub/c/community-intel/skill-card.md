## Description: <br>
Automates community intelligence gathering for open-source projects and products by searching Reddit, Hacker News, Twitter/X, GitHub, and YouTube for mentions, use cases, tips, complaints, and trends, then compiling structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npfaerber](https://clawhub.ai/user/npfaerber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and product teams use this skill to monitor community sentiment, adoption patterns, use cases, complaints, security mentions, and ecosystem trends for a target project or product. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled monitoring can repeatedly collect and store stale, inaccurate, or sensitive community findings. <br>
Mitigation: Confirm the cron schedule and INTEL_FILE location before enabling automation, and periodically review stored reports for sensitive, stale, or inaccurate content. <br>
Risk: Optional Discord or email delivery can send reports to unintended recipients if channels or addresses are misconfigured. <br>
Mitigation: Verify Discord channel IDs and email recipients before enabling report delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/npfaerber/community-intel) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with YAML, JSON, and bash configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append findings to a configured local intel file and optionally deliver summaries to Discord or email.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
