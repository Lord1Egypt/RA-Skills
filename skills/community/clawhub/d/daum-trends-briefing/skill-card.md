## Description: <br>
Fetch Daum real-time trend TOP10, add one-line context (top news title) + links, and print a 12-line briefing suitable for OpenClaw cron + Telegram announce. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunkim](https://clawhub.ai/user/hunkim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to generate concise Daum real-time trend briefings for scheduled OpenClaw cron runs and Telegram announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring Telegram announcements may post to the wrong chat or run on an unintended schedule if optional cron settings are copied without review. <br>
Mitigation: Verify the Telegram chat ID, cron schedule, timezone, and workspace path before enabling the optional recurring job. <br>
Risk: Daum page availability or markup changes can affect the generated briefing content. <br>
Mitigation: Review scheduled briefing output and monitor the cron job for collection failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hunkim/daum-trends-briefing) <br>
- [Daum Homepage](https://www.daum.net/) <br>
- [Daum Search](https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=<keyword>) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text briefing plus Markdown documentation with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints exactly 12 lines: title, 10 trend lines, and updatedAt.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
