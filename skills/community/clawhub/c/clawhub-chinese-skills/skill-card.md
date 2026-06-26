## Description: <br>
从 ClawHub 最新上传的 skill 中筛选中文用户上传的 skill 并汇报给用户。当用户要求查看最新中文 skill、查看新上传的中文技能、或类似需求时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0nsense11](https://clawhub.ai/user/n0nsense11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find recently uploaded ClawHub skills with Chinese titles or descriptions and return a concise list of matching links. When explicitly requested, it can help configure a daily ClawHub monitoring report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily reports can continue unexpectedly if a recurring cron job is created without clear user intent or an incorrect delivery target. <br>
Mitigation: Enable scheduled reports only after confirming the schedule and recipient/channel, then show how to list, test, update, or remove the cron job. <br>
Risk: The skill depends on public ClawHub page content and browser extraction, so transient page loading issues may produce incomplete results. <br>
Mitigation: Retry after loading the newest skills page, and tell the user when no Chinese skills are found on the current page instead of implying none exist globally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n0nsense11/clawhub-chinese-skills) <br>
- [ClawHub newest skills listing](https://clawhub.ai/skills?sort=newest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown list with links and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled-report setup guidance when the user asks for daily monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
